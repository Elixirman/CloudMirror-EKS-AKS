resource "aws_db_subnet_group" "this" {
  name       = "${var.project_name}-db-subnet"
  subnet_ids = module.vpc.private_subnets
}

resource "aws_security_group" "rds" {
  name        = "${var.project_name}-rds-sg"
  description = "Allow Postgres from EKS nodes"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [module.eks.node_security_group_id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "random_password" "db" {
  length  = 20
  special = false
}

resource "aws_db_instance" "this" {
  identifier             = "${var.project_name}-db"
  engine                 = "postgres"
  engine_version         = "16.9"
  instance_class         = "db.t3.micro"
  allocated_storage      = 20
  db_name                = "appdb"
  username               = "appuser"
  password               = random_password.db.result
  db_subnet_group_name   = aws_db_subnet_group.this.name
  vpc_security_group_ids = [aws_security_group.rds.id]
  publicly_accessible    = false
  skip_final_snapshot    = true
  deletion_protection    = false
}

output "rds_endpoint" {
  value = aws_db_instance.this.endpoint
}

output "db_password" {
  value     = random_password.db.result
  sensitive = true
}
