import replicate
import requests
import os

def get_incremented_filename(base_filename, extension):
    i = 1

    while os.path.exists(f"{base_filename}-{i}{extension}"):
        i += 1

    new_filename = f"{base_filename}-{i}{extension}"
    return new_filename

def create_image(prompt,filename):
    def get_incremented_filename(base_filename, extension):
        i = 1

        while os.path.exists(f"{base_filename}-{i}{extension}"):
            i += 1

        new_filename = f"{base_filename}-{i}{extension}"
        return new_filename

    model = replicate.models.get("stability-ai/stable-diffusion")
    version = model.versions.get("db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf")

    # https://replicate.com/stability-ai/stable-diffusion/versions/db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf#input
    inputs = {
        # Input prompt
        'prompt': prompt,

        # pixel dimensions of output image
        'image_dimensions': "768x768",

        # Specify things to not see in the output
        # 'negative_prompt': ...,

        # Number of images to output.
        # Range: 1 to 4
        'num_outputs': 1,

        # Number of denoising steps
        # Range: 1 to 500
        'num_inference_steps': 50,

        # Scale for classifier-free guidance
        # Range: 1 to 20
        'guidance_scale': 7.5,

        # Choose a scheduler.
        'scheduler': "DPMSolverMultistep",

        # Random seed. Leave blank to randomize the seed
        # 'seed': ...,
    }
    output= version.predict(**inputs)
    separator=''
    output=separator.join(output)
    print(output)
    response = requests.get(output)
    #filename=get_incremented_filename('image','.png')
    filename='image.png'
    with open(filename, 'wb') as f:
        f.write(response.content)
    return filename
# https://replicate.com/stability-ai/stable-diffusion/versions/db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf#output-schema


