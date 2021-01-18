variable ecr_repositories {
	type = map
	default = {
		repository_2 = {
			name                 = "bar2"
			image_tag_mutability = "MUTABLE"

			scan_on_push = true
		},
		repository_1 = {
			name                 = "bar3"
			image_tag_mutability = "MUTABLE"

			scan_on_push = false
		}

	}
}

