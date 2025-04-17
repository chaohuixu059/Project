import json
import xml.dom.minidom as minidom
import xml.etree.ElementTree as ET
import requests

def read_and_convert_to_json(file_url=None, local_file_path=None):
    movies_list = []
    
    if file_url:
        response = requests.get(file_url)
        content = response.text
    elif local_file_path:
        with open(local_file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    else:
        print("Error: No file source provided")
        return None
    
    movie_blocks = content.strip().split('\n\n')
    
    for block in movie_blocks:
        lines = block.strip().split('\n')
        movie_data = {"Movie": []}
        
        current_title = None
        current_genre = None
        current_studio = None
        current_year = None
        directors = []
        
        for line in lines:
            if not line.strip():
                continue
                
            parts = line.split(':', 1)
            if len(parts) < 2:
                continue
                
            key = parts[0].strip()
            value = parts[1].strip()
            
            if key == "Title":
                current_title = value
            elif key == "Genre":
                current_genre = value
            elif key == "Director Name":
                directors.append({"Name": value})
            elif key == "Studio":
                current_studio = value
            elif key == "Year":
                try:
                    current_year = int(value)
                except ValueError:
                    current_year = value
        
        if current_title:
            movie_data["Movie"].append({"Title": current_title})
        if current_genre:
            movie_data["Movie"].append({"Genre": current_genre})
        for director in directors:
            movie_data["Movie"].append({"Director": director})
        if current_studio:
            movie_data["Movie"].append({"Studio": current_studio})
        if current_year:
            movie_data["Movie"].append({"Year": current_year})
        
        movies_list.append(movie_data)
    
    with open('Movies.json', 'w', encoding='utf-8') as json_file:
        json.dump(movies_list, json_file, indent=2)
    
    print("Movies =")
    print(json.dumps(movies_list, indent=2))
    
    return movies_list

def sort_movies(movies_list, sort_key):
    def get_sort_value(movie):
        movie_info = movie["Movie"]
        
        if sort_key == "Title":
            for item in movie_info:
                if "Title" in item:
                    return item["Title"].lower()
        
        elif sort_key == "Genre":
            for item in movie_info:
                if "Genre" in item:
                    return item["Genre"].lower()
        
        elif sort_key == "Director":
            for item in movie_info:
                if "Director" in item:
                    return item["Director"]["Name"].lower()
        
        elif sort_key == "Studio":
            for item in movie_info:
                if "Studio" in item:
                    return item["Studio"].lower()
        
        elif sort_key == "Year":
            for item in movie_info:
                if "Year" in item:
                    return item["Year"]
        
        return ""
    
    sorted_movies = sorted(movies_list, key=get_sort_value)
    
    with open(f'MoviesSorted.json', 'w', encoding='utf-8') as json_file:
        json.dump(sorted_movies, json_file, indent=2)
    
    print(f"Movies sorted by {sort_key} =")
    print(json.dumps(sorted_movies, indent=2))
    
    return sorted_movies

def xml_generation(sorted_movies):
    root = ET.Element("Movies")
    
    for movie_data in sorted_movies:
        movie_elem = ET.SubElement(root, "Movie")
        
        for item in movie_data["Movie"]:
            if "Title" in item:
                title_elem = ET.SubElement(movie_elem, "Title")
                title_elem.text = item["Title"]
            
            elif "Genre" in item:
                genre_elem = ET.SubElement(movie_elem, "Genre")
                genre_elem.text = item["Genre"]
            
            elif "Director" in item:
                director_elem = ET.SubElement(movie_elem, "Director")
                name_elem = ET.SubElement(director_elem, "Name")
                name_elem.text = item["Director"]["Name"]
            
            elif "Studio" in item:
                studio_elem = ET.SubElement(movie_elem, "Studio")
                studio_elem.text = item["Studio"]
            
            elif "Year" in item:
                year_elem = ET.SubElement(movie_elem, "Year")
                year_elem.text = str(item["Year"])
    
    
    rough_string = ET.tostring(root, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent="  ")
    
    with open('Movies.xml', 'w', encoding='utf-8') as xml_file:
        xml_file.write(pretty_xml)
    
    print("XML file created: Movies.xml")

def main():
    local_file_path = "Movies.txt"
    movies_list = read_and_convert_to_json(local_file_path=local_file_path)
    if movies_list:
        sorted_movies = sort_movies(movies_list, "Title")
        xml_generation(sorted_movies)

if __name__ == "__main__":
    main()
