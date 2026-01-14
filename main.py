from loaders.registry import DatasetRegistry

reg = DatasetRegistry("Adverse-Weather-and-Low-Light-Vision-Datasets/datasets/datasets.csv")

reg.pretty(1)
# -> "[1] allweather - TRANSWEATHER (Multi-weather (rain+snow), ~19000 images)"

url = reg.link(1)   # main download link
meta = reg.get(31)  # ExDark metadata

print(f"Dataset URL: {url}")
print(f"Dataset Name: {meta['NAME']}")
print(f"Dataset Description: {meta['DESCRIPTION']}")
print(f"Dataset Size: {meta['SIZE']}")