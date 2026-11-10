# AI Animation Studio

First experiment: a small original 3D robot (Pip) waving beside a mysterious jar.

## Render without installing Blender

1. Open the **Actions** tab of this repository.
2. Select **Render First 3D Film**.
3. Click **Run workflow**, then **Run workflow** again.
4. When the run finishes with a green check, open it.
5. Under **Artifacts**, download **pip-first-film**. Unzip it to find the MP4.

The GitHub-hosted computer installs Blender and renders on the **CPU**, not a GPU. The first video is intentionally small (480 × 854, 12 fps, four seconds). Rendering may be slow and Actions availability/usage is subject to GitHub limits.

Files: `scene.py` controls the animation; `.github/workflows/render.yml` instructs GitHub how to render.
