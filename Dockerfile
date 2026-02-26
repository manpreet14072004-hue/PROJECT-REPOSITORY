FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY environment.yml .
COPY scripts/ ./scripts/

# Install miniconda
RUN curl -L https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -o miniconda.sh && \
    bash miniconda.sh -b -p /opt/conda && \
    rm miniconda.sh

# Set conda path
ENV PATH=/opt/conda/bin:$PATH

# Create conda environment
RUN conda env create -f environment.yml
RUN echo "source activate project-env" > ~/.bashrc

# Copy project files
COPY . .

# Set entrypoint
ENTRYPOINT ["conda", "run", "-n", "project-env", "python", "scripts/run_pipeline.py"]
