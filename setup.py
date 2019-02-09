import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="examgen",
    version="0.1",
    author="Yuri Malheiros",
    author_email="yuri@dcx.ufpb.br",
    description="Generate exams using Markdown and Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yurimalheiros/examgen",
    packages=setuptools.find_packages(),
    package_data={"examgen": ["template/*.md", "template/*.css"]},
    install_requires=["click", "PyPDF2"],
    entry_points={"console_scripts": ["examgen=examgen.cli:generate"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)