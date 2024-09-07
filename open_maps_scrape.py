import requests
import xml.etree.ElementTree as ET
import pandas as pd


def get_residential_addresses(bb_bottom_left, bb_top_right):
    """
    :param bb_bottom_left: [lat, lon] of bounding box bottom left point
    :param bb_top_right: [lat, lon] of bounding box rop right point
    :return: pd.DataFrame of residential addresses within the coordinate bounding box
    """

    #init requests session
    with requests.Session() as s:

        s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0'

        #build query string to openstreetmap API
        url = "https://api.openstreetmap.org/"
        url += f'/api/0.6/map?bbox={bb_bottom_left[1]},{bb_bottom_left[0]},{bb_top_right[1]},{bb_top_right[0]}'

        #query API and notify user of bad status
        r = requests.get(url)
        print(f'Open Street Maps request returned status: {r.status_code}')
        if r.status_code != 200:
            print(f'Status message: {r.text}')

        #load XML
        root = ET.fromstring(r.text)

        data = []

        #XML extraction to dictionary
        for way in root.findall('way'):

            way_data = way.attrib

            # Extract 'tag' elements into a dictionary
            tags = {tag.attrib['k']: tag.attrib['v'] for tag in way.findall('tag')}
            way_data.update(tags)

            data.append(way_data)

        #create DataFrame and strip unnecessary columns and null vals
        df = pd.DataFrame(data)

        #the API returns unstructured data - need to check whether the columns of interest exist in the data
        necessary_columns = ['addr:city', 'addr:housenumber', 'addr:postcode', 'addr:state', 'addr:street', 'source', 'building']
        for col in necessary_columns:
            if col not in df.columns:
                return None
            else:
                pass

        #clean the data of null address values
        df = df.dropna(subset=['addr:state'])
        df = df[df['building']=='yes']
        df = df[['addr:city', 'addr:housenumber', 'addr:postcode', 'addr:state', 'addr:street', 'source']]

        #create streetAddress column which will be used to query zillow later
        df['addr:streetAddress'] = df.apply(
            lambda
                row: f"{row.get('addr:housenumber', '')} {row.get('addr:street', '')}".strip(),
            axis=1
        )

        #rename columns
        new_columns = ['city', 'houseNumber', 'zipcode', 'state', 'street', 'source', 'streetAddress']
        df.columns = new_columns

        return df

if __name__ == "__main__":
    bb_bottom_left = [33.66772764797897, -112.30735141606544]
    bb_top_right = [33.757544665988554, -112.10848170826618]

    df = get_residential_addresses(bb_bottom_left,bb_top_right)