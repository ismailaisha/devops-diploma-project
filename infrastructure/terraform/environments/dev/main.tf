data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }

  filter {
    name = "virtualization-type"
    values = ["hvm"]
  }
  
}

data "http" "my_ip" {
  url = "https://ipv4.icanhazip.com"
}

resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support = true

  tags = {
    Name = "$(var.project_name)-vpc"
    Environment = var.environment
    Project = var.project_name
  }
}

resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "${var.aws_region}a"
  map_public_ip_on_launch = true

  tags = {
    Name = "$(var.project_name)-public-subnet"
    Environment = var.environment
    Project = var.project_name
  }
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "$(var.project_name)-igw"
    Environment = var.environment
    Project = var.project_name
  }
  
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }

  tags = {
    Name = "$(var.project_name)-public-rt"
    Environment = var.environment
    Project = var.project_name
  }
}

resource "aws_route_table_association" "public" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
  
}

resource "aws_security_group" "app_server" {
  name        = "$(var.project_name)-app-sg"
  description = "Security group for $(var.project_name)"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow HTTP traffic from anywhere"
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow HTTPS traffic from anywhere"
  }

 # API порт — доступен всем
  ingress {
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "FastAPI"
  }

  # SSH — только с твоего IP
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["${chomp(data.http.my_ip.response_body)}/32"]
    description = "SSH only from my IP"
  }

  # WireGuard VPN
  ingress {
    from_port   = 51820
    to_port     = 51820
    protocol    = "udp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "WireGuard VPN"
  }

  # Исходящий трафик — всё разрешено
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "All outbound traffic"
  }

  tags = {
    Name        = "${var.project_name}-app-sg"
    Environment = var.environment
    Project     = var.project_name
  }
}

# ─────────────────────────────────────────
# Security Group для Jenkins Server
# ─────────────────────────────────────────
resource "aws_security_group" "jenkins" {
  name        = "${var.project_name}-jenkins-sg"
  description = "Security group for FitFlow Jenkins Server"
  vpc_id      = aws_vpc.main.id

  # Jenkins UI — только с твоего IP
  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["${chomp(data.http.my_ip.response_body)}/32"]
    description = "Jenkins UI"
  }

  # SSH — только с твоего IP
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["${chomp(data.http.my_ip.response_body)}/32"]
    description = "SSH only from my IP"
  }

  # WireGuard VPN
  ingress {
    from_port   = 51820
    to_port     = 51820
    protocol    = "udp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "WireGuard VPN"
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "All outbound traffic"
  }

  tags = {
    Name        = "${var.project_name}-jenkins-sg"
    Environment = var.environment
    Project     = var.project_name
  }
}

resource "aws_key_pair" "fitflow" {
  key_name   = var.ssh_key_name
  public_key = file("~/.ssh/fitflow.pub")

  tags = {
    Name    = var.ssh_key_name
    Project = var.project_name
  }
}

# ─────────────────────────────────────────
# App Server — основной сервер приложения
# ─────────────────────────────────────────
resource "aws_instance" "app_server" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = var.instance_type
  subnet_id              = aws_subnet.public.id
  vpc_security_group_ids = [aws_security_group.app_server.id]
  key_name               = aws_key_pair.fitflow.key_name

  root_block_device {
    volume_size = 20
    volume_type = "gp3"
  }

  tags = {
    Name        = "${var.project_name}-app-server"
    Environment = var.environment
    Project     = var.project_name
    Role        = "app"
  }
  
  lifecycle {
    ignore_changes = [ami]
  }
}

# ─────────────────────────────────────────
# Jenkins Server — CI/CD сервер
# ─────────────────────────────────────────
resource "aws_instance" "jenkins" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = var.instance_type
  subnet_id              = aws_subnet.public.id
  vpc_security_group_ids = [aws_security_group.jenkins.id]
  key_name               = aws_key_pair.fitflow.key_name

  root_block_device {
    volume_size = 20
    volume_type = "gp3"
  }

  tags = {
    Name        = "${var.project_name}-jenkins"
    Environment = var.environment
    Project     = var.project_name
    Role        = "jenkins"
  }
  
  lifecycle {
    ignore_changes = [ami]
  }
}

# ─────────────────────────────────────────
# Elastic IP — статический публичный IP
# Не меняется при перезапуске сервера
# ─────────────────────────────────────────
resource "aws_eip" "app_server" {
  instance = aws_instance.app_server.id
  domain   = "vpc"

  tags = {
    Name    = "${var.project_name}-app-eip"
    Project = var.project_name
  }
}

resource "aws_eip" "jenkins" {
  instance = aws_instance.jenkins.id
  domain   = "vpc"

  tags = {
    Name    = "${var.project_name}-jenkins-eip"
    Project = var.project_name
  }
}

# ─────────────────────────────────────────
# S3 Bucket — хранилище для бэкапов БД
# ─────────────────────────────────────────
resource "aws_s3_bucket" "backups" {
  bucket        = var.s3_bucket_name
  force_destroy = true

  tags = {
    Name        = var.s3_bucket_name
    Environment = var.environment
    Project     = var.project_name
  }
}

# Закрываем публичный доступ к бэкапам
resource "aws_s3_bucket_public_access_block" "backups" {
  bucket = aws_s3_bucket.backups.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Версионирование — храним историю бэкапов
resource "aws_s3_bucket_versioning" "backups" {
  bucket = aws_s3_bucket.backups.id

  versioning_configuration {
    status = "Enabled"
  }
}

