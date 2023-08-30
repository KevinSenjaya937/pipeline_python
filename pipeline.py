import argparse
import json
from collections import namedtuple

PreferenceMatch = namedtuple("PreferenceMatch", ["product_name", "product_codes"])


def main(product_data, include_tags, exclude_tags):
    """The implementation of the pipeline test."""
    # Dictionary to group product codes by product name.
    matching_products = {}

    for product in product_data:

        # Check the include and exclude tags.
        if any(tag in product["tags"] for tag in include_tags) and not any(tag in product["tags"] for tag in exclude_tags):
            
            # Check if the product name already exists in the dictionary.
            # If it does not exist, initialize new entry. Inside will be a list with the product code.
            # If it exists, append the product code to the list under the product name.
            if product["name"] not in matching_products:
                matching_products[product["name"]] = [product["code"]]
            else:
                matching_products[product["name"]].append(product["code"])

    # Convert matching_products dictionary into a list of PreferenceMatch.
    # Get items in dictionary and convert to key value pairs, name(key) and codes(value).
    matches_found = [PreferenceMatch(name, codes) for name, codes in matching_products.items()]

    return matches_found


if __name__ == "__main__":

    def parse_tags(tags):
        return [tag for tag in tags.split(",") if tag]

    parser = argparse.ArgumentParser(
        description="Extracts unique product names matching given tags."
    )
    parser.add_argument(
        "product_data",
        help="a JSON file containing tagged product data",
    )
    parser.add_argument(
        "--include",
        type=parse_tags,
        help="a comma-separated list of tags whose products should be included",
        default="",
    )
    parser.add_argument(
        "--exclude",
        type=parse_tags,
        help="a comma-separated list of tags whose matching products should be excluded",
        default="",
    )

    args = parser.parse_args()

    with open(args.product_data) as f:
        product_data = json.load(f)

    order_items = main(product_data, args.include, args.exclude)

    for item in order_items:
        print("%s:\n%s\n" % (item.product_name, "\n".join(item.product_codes)))
