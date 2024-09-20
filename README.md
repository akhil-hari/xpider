
# Xpider

**Xpider** is a simple, scalable, distributed web scraping framework in Python that utilizes Redis and MongoDB for scaling.

## Installation

To install Xpider, clone the repository and run the installation command:

```bash
git clone https://github.com/akhil-hari/xpider.git
cd xpider
pip install .
```

## Xpider CLI

Xpider comes with a CLI tool that you can use to create and run Xpider projects.

### Creating a New Xpider Project

You can create a new Xpider project using the `xpider new` command:

```bash
xpider new <project_name>
```

### Running a Xpider Project

To run a Xpider project, use the `xpider run` command. By default, this command will run the project in the current working directory and use CSV files to store data while utilizing Python's built-in features to queue requests—ideal for local testing.

For scaling across multiple instances, you can provide a Redis URL and a MongoDB URL using the `--redis-url` and `--mongo-url` flags, respectively, or by setting the `XPIDER_REDIS_URL` and `XPIDER_MONGO_URL` environment variables.

#### Command Usage

```bash
xpider run [-h] [--path PATH] [--mongo-url MONGO_URL] [--redis-url REDIS_URL]
```

#### Options



- `--path PATH`  
  Path to the Xpider project directory.

- `--mongo-url MONGO_URL`  
  MongoDB URL to store scraped data.

- `--redis-url REDIS_URL`  
  Redis URL for queuing requests.

## Note

This repository is under active development. The features and commands mentioned here may be updated in the future.