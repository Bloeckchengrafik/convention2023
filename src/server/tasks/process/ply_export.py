def ply_export(dots: list[tuple[float, float, float]]):
    # Step 1: Simplify the dots (int conversion and remove duplicates)
    dots = [(int(x), int(y), int(z)) for x, y, z in dots]
    dots = list(set(dots))

    # Step 3: Create the PLY file
    with open("export.ply", "w") as f:
        f.write("ply\n")
        f.write("format ascii 1.0\n")
        f.write("comment yay!\n")
        f.write(f"element vertex {len(dots)}\n")
        f.write("property float x\n")
        f.write("property float y\n")
        f.write("property float z\n")
        f.write("end_header\n")
        for x, y, z in dots:
            f.write(f"{x} {y} {z}\n")
