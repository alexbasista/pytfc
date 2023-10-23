#------------------------------------------------------------------------------
# Variables
#------------------------------------------------------------------------------
variable "pet_length" {
  type    = number
  default = 3
}

variable "pet_prefix" {
  type    = string
  default = "test"
}

variable "pet_separator" {
  type    = string
  default = "-"
}

#------------------------------------------------------------------------------
# Resources
#------------------------------------------------------------------------------
resource "random_pet" "test0" {
  length    = var.pet_length
  prefix    = var.pet_prefix
  separator = var.pet_separator
}

resource "random_pet" "test1" {
  length    = var.pet_length
  prefix    = var.pet_prefix
  separator = var.pet_separator
}

resource "random_pet" "test2" {
  length    = var.pet_length
  prefix    = var.pet_prefix
  separator = var.pet_separator
}

resource "random_pet" "test3" {
  length    = var.pet_length
  prefix    = var.pet_prefix
  separator = var.pet_separator
}

resource "random_pet" "test4" {
  length    = var.pet_length
  prefix    = var.pet_prefix
  separator = var.pet_separator
}

resource "random_pet" "test5" {
  length    = var.pet_length
  prefix    = var.pet_prefix
  separator = var.pet_separator
}

resource "random_pet" "test6" {
  length    = var.pet_length
  prefix    = var.pet_prefix
  separator = var.pet_separator
}

resource "random_pet" "test7" {
  length    = var.pet_length
  prefix    = var.pet_prefix
  separator = var.pet_separator
}

resource "random_pet" "test8" {
  length    = var.pet_length
  prefix    = var.pet_prefix
  separator = var.pet_separator
}

resource "random_pet" "test9" {
  length    = var.pet_length
  prefix    = var.pet_prefix
  separator = var.pet_separator
}

resource "random_pet" "testa" {
  length    = var.pet_length
  prefix    = var.pet_prefix
  separator = var.pet_separator
}

resource "random_pet" "testb" {
  length    = var.pet_length
  prefix    = var.pet_prefix
  separator = var.pet_separator
}

resource "random_pet" "testc" {
  length    = var.pet_length
  prefix    = var.pet_prefix
  separator = var.pet_separator
}

resource "random_pet" "testd" {
  length    = var.pet_length
  prefix    = var.pet_prefix
  separator = var.pet_separator
}

resource "random_pet" "teste" {
  length    = var.pet_length
  prefix    = var.pet_prefix
  separator = var.pet_separator
}

resource "random_pet" "testf" {
  length    = var.pet_length
  prefix    = var.pet_prefix
  separator = var.pet_separator
}

resource "random_pet" "testg" {
  length    = var.pet_length
  prefix    = var.pet_prefix
  separator = var.pet_separator
}

#------------------------------------------------------------------------------
# Outputs
#------------------------------------------------------------------------------
output "test0" {
  value = random_pet.test0.id
}

output "test1" {
  value     = random_pet.test1.id
  sensitive = true
}