def land_upload_path(instance, filename):
    farmer_name = instance.farmer.name.replace(" ", "_").lower()
    return f"land/{farmer_name}/{filename}"