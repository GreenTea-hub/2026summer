from pathlib import Path
import shutil

def organize_desktop():
    # 1. 获取桌面路径（自动适配 Windows/Mac）
    desktop = Path.home() / "Desktop"

    # 2. 定义扩展名 -> 目标文件夹的映射
    type_map = {
        "Images":    [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg"],
        "Documents": [".pdf", ".doc", ".docx", ".txt", ".ppt", ".pptx", ".xls", ".xlsx"],
        "Videos":    [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv"],
        "Music":     [".mp3", ".wav", ".flac", ".aac", ".ogg"],
        "Archives":  [".zip", ".rar", ".7z", ".tar", ".gz"],
        "Programs":  [".exe", ".msi", ".bat", ".cmd"],
    }

    # 3. 反向映射：扩展名 -> 文件夹名，方便 O(1) 查找
    ext_to_folder = {}
    for folder, exts in type_map.items():
        for ext in exts:
            ext_to_folder[ext.lower()] = folder

    # 4. 脚本自身文件名，避免运行时把自己也移走
    script_name = Path(__file__).name

    moved_count = 0
    category_count = {}

    # 5. 遍历桌面所有条目
    for item in desktop.iterdir():
        # 跳过文件夹（只处理文件）
        if item.is_dir():
            continue

        # 跳过脚本自身 + 隐藏文件
        if item.name == script_name or item.name.startswith("."):
            continue

        # 6. 获取扩展名并匹配目标文件夹
        ext = item.suffix.lower()
        folder_name = ext_to_folder.get(ext, "Others")

        # 7. 创建目标文件夹（已存在则跳过）
        target_folder = desktop / folder_name
        target_folder.mkdir(exist_ok=True)

        # 8. 处理同名文件冲突：自动重命名
        target_path = target_folder / item.name
        if target_path.exists():
            stem = item.stem          # 不含扩展名的文件名
            counter = 1
            while target_path.exists():
                new_name = f"{stem}_{counter}{ext}"
                target_path = target_folder / new_name
                counter += 1

        # 9. 移动文件
        shutil.move(str(item), str(target_path))
        moved_count += 1
        category_count[folder_name] = category_count.get(folder_name, 0) + 1
        print(f"Moved: {item.name} -> {folder_name}/")

    # 10. 输出统计
    print(f"\nDone! Total moved: {moved_count}")
    for folder, count in sorted(category_count.items()):
        print(f"  {folder}: {count}")


if __name__ == "__main__":
    organize_desktop()