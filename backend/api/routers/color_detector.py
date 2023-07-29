from fastapi import FastAPI, UploadFile, APIRouter
from PIL import Image
from sklearn.cluster import KMeans
import numpy as np
import io
import webcolors
from api.response import ApiResponse

router = APIRouter(prefix="")


def find_dominant_color(image_path, num_colors=1):
    # Load the image
    image = Image.open(image_path)

    # Resize the image to speed up processing (optional)
    image = image.resize((100, 100))

    # Convert image to RGB
    image = image.convert('RGB')

    # Flatten the image to a 1D array of RGB values
    pixels = np.array(image).reshape(-1, 3)

    # Perform K-means clustering
    kmeans = KMeans(n_clusters=num_colors)
    kmeans.fit(pixels)

    # Get the RGB values of the dominant colors
    dominant_colors = kmeans.cluster_centers_

    return dominant_colors
# def closest_colour(requested_colour):
#     min_colours = {}
#     for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
#         r_c, g_c, b_c = webcolors.hex_to_rgb(key)
#         rd = (r_c - requested_colour[0]) ** 2
#         gd = (g_c - requested_colour[1]) ** 2
#         bd = (b_c - requested_colour[2]) ** 2
#         min_colours[(rd + gd + bd)] = name
#     return min_colours[min(min_colours.keys())]

def closest_colour(requested_colour):
    min_colours = {}
    common_color_json = get_common_color_json()
    for name, rgb in common_color_json.items():
        r_c, g_c, b_c = rgb
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]

def get_colour_name(requested_colour):
    try:
        closest_name = actual_name = webcolors.rgb_to_name(requested_colour)
    except ValueError:
        closest_name = closest_colour(requested_colour)
        actual_name = None
    return actual_name, closest_name


@router.post("/detect-color")
async def upload_file(image: UploadFile):
    try:
        # Read the uploaded file
        image_bytes = await image.read()

        # Create an in-memory stream from the image bytes
        image_stream = io.BytesIO(image_bytes)

        # Find the dominant color
        dominant_color = find_dominant_color(image_stream)
        # rgb_values = tuple([int(component) for component in dominant_color[0]])
        rgb_values = tuple(dominant_color.tolist()[0])

        actual_name, closest_name = get_colour_name(rgb_values)
        data = {"color": closest_name}
        return ApiResponse.response_ok(data=data)
    except Exception as e:
        print(e)
        ApiResponse.response_internal_server_error(e=str(e))



def get_common_color_json():
    common_colors = [
        'aliceblue', 'antiquewhite', 'aqua', 'aquamarine', 'azure', 'beige', 'bisque',
        'black', 'blanchedalmond', 'blue', 'blueviolet', 'brown', 'burlywood', 'cadetblue',
        'chartreuse', 'chocolate', 'coral', 'cornflowerblue', 'cornsilk', 'crimson', 'cyan',
        'darkblue', 'darkcyan', 'darkgoldenrod', 'darkgray', 'darkgreen', 'darkkhaki', 'darkmagenta',
        'darkolivegreen', 'darkorange', 'darkorchid', 'darkred', 'darksalmon', 'darkseagreen',
        'darkslateblue', 'darkslategray', 'darkturquoise', 'darkviolet', 'deeppink', 'deepskyblue',
        'dimgray', 'dodgerblue', 'firebrick', 'floralwhite', 'forestgreen', 'fuchsia', 'gainsboro',
        'ghostwhite', 'gold', 'goldenrod', 'gray', 'green', 'greenyellow', 'honeydew', 'hotpink',
        'indianred', 'indigo', 'ivory', 'khaki', 'lavender', 'lavenderblush', 'lawngreen', 'lemonchiffon',
        'lightblue', 'lightcoral', 'lightcyan', 'lightgoldenrodyellow', 'lightgray', 'lightgreen',
        'lightpink', 'lightsalmon', 'lightseagreen', 'lightskyblue', 'lightslategray', 'lightsteelblue',
        'lightyellow', 'lime', 'limegreen', 'linen', 'magenta', 'maroon', 'mediumaquamarine',
        'mediumblue', 'mediumorchid', 'mediumpurple', 'mediumseagreen', 'mediumslateblue',
        'mediumspringgreen', 'mediumturquoise', 'mediumvioletred', 'midnightblue', 'mintcream',
        'mistyrose', 'moccasin', 'navajowhite', 'navy', 'oldlace', 'olive', 'olivedrab',
        'orange', 'orangered', 'orchid', 'palegoldenrod', 'palegreen', 'paleturquoise', 'palevioletred',
        'papayawhip', 'peachpuff', 'peru', 'pink', 'plum', 'powderblue', 'purple', 'red',
        'rosybrown', 'royalblue', 'saddlebrown', 'salmon', 'sandybrown', 'seagreen', 'seashell',
        'sienna', 'silver', 'skyblue', 'slateblue', 'slategray', 'snow', 'springgreen', 'steelblue',
        'tan', 'teal', 'thistle', 'tomato', 'turquoise', 'violet', 'wheat', 'white', 'whitesmoke',
        'yellow', 'yellowgreen'
    ]
    color_dict = {}

    for color_name in common_colors:
        try:
            rgb = webcolors.name_to_rgb(color_name)
            color_dict[color_name] = rgb
        except ValueError:
            # If the color name is not recognized, skip it
            pass

    return color_dict

