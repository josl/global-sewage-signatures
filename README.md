# Grouping of global sewage samples based on DNA signatures

## Description

We have a dataset containing DNA from 84 sewage samples around the world. These sewage samples contain a large amount of DNA from different bacteria and organisms. DNA can be represented as long sequences of the letters ATGC. For each sample we have split up the sequences into sub-sequences of length 16\. These sub-sequences can be stored into a bit-array of length 4^16 (all possible 16 length DNA sequences). So for our 84 samples we have 84 bit-arrays of size ~500mb each, which corresponds to a final matrix of size ~43 gb.

We would like to be able to cluster these 84 samples into geographical locations based on DNA sequences. The challenge is that we have many features (4^16) and 84 samples. Our plan is to use Redis to store the bit-arrays and DBSCAN to cluster the samples together. We use Redis as it is a NoSQL database that supports bit-arrays. We want to speed-up the regionQuery-part (neighbor-finding-part) of DBSCAN by implementing LSH for MinHash signatures. We will also try to see if we can use MapReduce to calculate the neighbors for each sample and compare the runtime with the LSH for MinHash approach. While it may seem unnecessary to speed up DBSCAN for 84 samples, more and more data is produced for this project in the future, so it is important to make it ready for this challenge.

The main goal is to investigate if it is possible to group samples together geographically based on the DNA sequences present in the samples. Our data is labelled so we can validate the clusters.

## Installation

If you prefer to avoid installing redis yourself we provide a Docker container. Follow the instructions here:

```bash
# Build Docker images
docker build -t sewage-signatures .

# Run container
docker run --name sewage-redis -d sewage-signatures
```

If redis is install you need to start an instance of the database on port 4444

```bash
make redis
```

Then, you need to create a Redis Protocol file with all your redis comands

```bash
./scripts/mass_insertion.py --folder=/home/projects/cge/people/olund/projects/sewage/sewage5/ --output=dataset/redis_protocol.txt
```

```bash
./scripts/mass_insertion.py --folder=/home/projects/cge/people/olund/projects/sewage/sewage5/ --output=dataset/redis_protocol.txt
```

## General Comands for Development

It's recommended to create a virtual environment (conda env preffered)

General commands:

- "make list" to list all available targets;
- "make setup" to install all dependencies (do not forget to create a virtualenv first);
- "make test" to test your application (tests in the tests/ directory);
- "make tox" to run tests against all supported python versions.

## License

MIT © [Jose Luis Bellod Cisneros](http://josl.github.i- o)
