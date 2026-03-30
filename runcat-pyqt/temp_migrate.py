import os
import shutil

base_dir = r"e:\AI_Projects\RunCat365\runcat-pyqt\resources\runners"
runners = ['cat', 'horse', 'parrot']

for runner in runners:
    runner_dir = os.path.join(base_dir, runner)
    size_dir = os.path.join(runner_dir, '32x32')
    os.makedirs(size_dir, exist_ok=True)
    
    for filename in os.listdir(runner_dir):
        if filename == '32x32':
            continue
        if not filename.endswith('.png'):
            continue
        
        parts = filename.split('.')[0].split('_')
        if len(parts) == 2:
            try:
                idx = int(parts[1])
                old_path = os.path.join(runner_dir, filename)
                new_path = os.path.join(size_dir, f'frame_{idx}.png')
                if not os.path.exists(new_path):
                    shutil.move(old_path, new_path)
                    print(f"Moved {old_path} -> {new_path}")
            except ValueError:
                continue

print("Done")
