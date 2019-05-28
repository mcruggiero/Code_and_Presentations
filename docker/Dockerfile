# 1. reference: https://hub.docker.com/_/ubuntu/
FROM ubuntu:16.04

# 2. Adds metadata to the image as a key value pair example LABEL version="1.0"
LABEL maintainer="Michael Ruggiero <michael@mcruggiero.com>"

# 3. Set environment variables
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

# 4. Create empty directory to attach volume
RUN mkdir ~/GitProjects

# 5. Install Ubuntu packages
RUN apt-get update && apt-get install -y \
    wget \
    bzip2 \
    ca-certificates \
    build-essential \
    curl \
    git-core \
    htop \
    pkg-config \
    unzip \
    unrar \
    tree \
    freetds-dev

# 6. Clean up
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# 7. Install Anaconda
RUN echo 'export PATH=/opt/conda/bin:$PATH' > /etc/profile.d/conda.sh

# 8. Anaconda in Shell
RUN wget --quiet https://repo.anaconda.com/archive/Anaconda3-5.2.0-Linux-x86_64.sh -O ~/anaconda.sh

# 9. Conda Installs
RUN /bin/bash ~/anaconda.sh -b -p /opt/conda

# 10. Conda Clean
RUN rm ~/anaconda.sh

# 11. Set path to conda
ENV PATH /opt/conda/bin:$PATH

# 12. Update Anaconda
RUN conda update conda && conda update anaconda && conda update --all

# 13. Install other Python packages
RUN conda install pymssql

# 14. More packages installed
RUN pip install SQLAlchemy \
    missingno \
    json_tricks \
    bcolz \
    gensim \
    elasticsearch \
    psycopg2-binary \
    pandas

# 15. Configure access to Jupyter
WORKDIR /root/GitProjects
EXPOSE 8888
CMD jupyter lab --no-browser --ip=0.0.0.0 --allow-root --NotebookApp.token='data-science'