# Virtual-Angle-Finder

The program helps to easily find the angle within any given image. 
Click on 3 points to find the angle between them. The first point is considered as the origin.
Use mouse left button to register each point and double click mouse right button to remove the previous point.
You can press 'r' to remove all the points and 'q' to quit the program.

## Requirements

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the following.

```bash
pip install opencv-python
pip install argparse
```

## Usage

```python
python virtualAngleFinder.py --path image_path
