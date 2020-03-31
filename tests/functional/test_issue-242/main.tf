provider "gsuite" {
  oauth_scopes = [
    "https://www.googleapis.com/auth/admin.directory.group",
    "https://www.googleapis.com/auth/admin.directory.user"
  ]
}

resource "gsuite_group" "my-group-i" {
  email       = "my-group-i@mydomain.com"
  name        = "My Group I"
}

resource "gsuite_group" "my-group-ii" {
  email       = "my-group-ii@mydomain.com"
  name        = "My Group II"
}