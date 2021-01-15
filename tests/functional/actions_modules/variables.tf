variable ecr_repositories {
	type = map
	default = {
		repository_1 = {
			name                 = "bar"
			image_tag_mutability = "MUTABLE"

			scan_on_push = true
		}
	}
}

variable repo_name {
	type = string
	default = "repository_1"
}

variable scan_on_push_val {
	type = bool
	default = true
}