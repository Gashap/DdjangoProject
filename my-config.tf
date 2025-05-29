variable "token" { type = string }
variable "cloud" { type = string }
variable "folder" { type = string }
variable "zone" { type = string }
variable "network" { type = string }
variable "vpc_name" { type = string }
variable "def_zone" { type = string }
variable "db_user" { type = string }
variable "db_password" { type = string }

terraform {
  required_providers {
    yandex = {
      source = "yandex-cloud/yandex"
    }
  }
}

provider "yandex" {
  token = var.token
  cloud_id = var.cloud
  folder_id = var.folder
  zone = var.zone
}

# Создание сервисного аккаунта
resource "yandex_iam_service_account" "service-for-site" {
  name = "service-for-site"
}

# Назначение ролей
resource "yandex_resourcemanager_folder_iam_member" "roles-for-site" {
  for_each = toset([
    "admin",
    "mdb.vuewer",
    "servless.containers.invoke",
    "servless.containers.editor",
    "vpc.publicAdmin",
    "compute.editor",
    "monitoring.editor",
    "storage.uploder",
    "api-geteway.editor"

  ])
  folder_id = var.folder
  member    = "serviceAccount:${yandex_iam_service_account.service-for-site.id}"
  role      = each.value
}

# Создание статического ключа сервисного аккаунта
resource "yandex_iam_service_account_static_access_key" "key-for-site" {
  service_account_id = yandex_iam_service_account.service-for-site.id
}

# Создание виртуальной сети
resource "yandex_vpc_network" "main" {
  name = var.vpc_name
}

# Создание подсети виртуальной сети
resource "yandex_vpc_subnet" "main" {
  name = "${var.vpc_name}-subnet"
  zone = var.def_zone
  network_id = yandex_vpc_network.main.id
  v4_cidr_blocks = [10.128.0.0/24]
}

# Container Registry, в котором будут храниться образы
resource "yandex_container_registry" "django-registry" {
  name      = "django-registry"
  folder_id = var.folder
}

resource "yandex_container_repository" "django-repo" {
  name = "${yandex_container_registry.django-registry.id}/django-app"
}

# Создание кластера Postgres
resource "yandex_mdb_postgresql_cluster" "db1" {
  environment = "PRODUCTION"
  name        = "vacanciesDB"
  network_id  = var.network

  config {
    version = "15"
    resources {
      disk_size = 10
      resource_preset_id = "b1.medium"
      disk_type_id = "network-hdd"
    }

    access {
      web_sql = true
      serverless = true
    }
  }

  host {
    zone = var.def_zone
    subnet_id = yandex_vpc_subnet.main.id
  }
}

# Добавление пользователя базы данных
resource "yandex_mdb_postgresql_user" "user" {
  cluster_id = yandex_mdb_postgresql_cluster.db1.id
  name       = var.db_user
  password   = var.db_password
}

# Добавление базы данных в кластер
resource "yandex_mdb_postgresql_database" "my_db" {
  cluster_id = yandex_mdb_postgresql_cluster.db1.id
  name       = "testdb"
  owner      = yandex_mdb_postgresql_user.user.name
  lc_collate = "C"
  lc_type    = "C"
}

resource "yandex_serverless_container" "project" {
  memory = 2048
  name   = "service-for-site"
  cores = 1
  service_account_id = yandex_iam_service_account.service-for-site.id
}