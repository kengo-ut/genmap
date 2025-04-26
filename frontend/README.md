# Frontend

## Setup

### Installation
Install Node.js / yarn with [Volta](https://volta.sh/)

```bash
volta install node
volta install yarn
```

Install dependencies

```bash
yarn
```

### Set env
Create a `.env.local` file and set the below url.

```
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000
```

### Place data
Create a `public/data/control_images` directory and place control images (canny, soft edge, depth, pose, or gray) used for controlling image generation in it.

### Run
```bash
yarn dev
```
