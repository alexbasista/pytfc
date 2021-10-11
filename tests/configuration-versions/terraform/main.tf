resource "random_pet" "test" {
  count     = 2
  length    = 3
  separator = "-"

  keepers = {
    always = timestamp()
  }
}