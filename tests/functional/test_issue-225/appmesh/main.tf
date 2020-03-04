resource "aws_appmesh_virtual_node" "vn" {
  for_each = {
    "ui": "demo2",
  }
  name      = "${each.key}-vn"
  mesh_name = each.value

  spec {
    backend {
      virtual_service {
        virtual_service_name = "servicea.simpleapp.local"
      }
    }

    listener {
      port_mapping {
        port     = 80
        protocol = "http"
      }
    }

    service_discovery {
      dns {
        hostname = "serviceb.simpleapp.local"
      }
    }
  }
}
