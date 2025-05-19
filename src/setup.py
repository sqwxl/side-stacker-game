from setuptools import setup, find_packages

setup(
    name="ssg",
    version="0.0.1",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "ssg_init_db=ssg:init_db",
            "ssg_train_ml=ssg.ai.training.train:main",
        ]
    },
)
