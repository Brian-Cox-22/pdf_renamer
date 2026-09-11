import os
from pypdf import PdfReader



class PDF_Metadata():
    def __init__(self, title, author, publication_date):
        self.title = title
        self.author = author
        self.publication_date = publication_date


# this is largely code from the learnLLM project on Boot.dev
def get_files_info(working_directory: str, directory: str = "."):
    '''
   Directory treated as local path within working_directory
   Used to limit scope.
   Takes up to two strings 
    '''
    
    working_path = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_path, directory))

    # check if a target directory is within the working path
    valid_target_dir = os.path.commonpath([working_path, target_dir]) == working_path

    if not valid_target_dir:
        # probably going to want to change this to a log instead
        return f'Error: Cannot work in "{directory}" as it is outside the permitted working directory'
    
    # check if is a directory that exists
    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'
    
    # directory_as_list = target_dir[1:].split('/')
    string_list = []
    for item in os.listdir(target_dir):
        full_path = os.path.join(target_dir, item)
        
        try:
            size = os.path.getsize(full_path)
        except:
            return f"Error: could not get {item} size"
        
        try:
            is_dir = os.path.isdir(full_path)
        except:
            return f"Error: could not check if {item} is a directory"
        
        string = f"- {item}: file_size={size} bytes, is_dir={is_dir}"
        string_list.append(string)

    return "\n".join(string_list)


# using pypdf to read metadata

def read_metadata(pdf_file: str):
    '''
    Takes a single path to a PDF as an input, checks if the PDF has metadata
    If the pdf does not have metadata, then OCR the PDF and sends the text to ??? to get the author, title (to be implimented)
    '''
    reader = PdfReader(pdf_file)

    # in all likelyhoot some of all of the metadata will be missing. Need to think about how to approach that.
    metadata = reader.metadata
    # options:
        # title, author, subject, creator, producer, creation_date, modification_date

    if not metadata:
        # This is where I need to figure out what to do with the lack of metadata
        if (len(reader.get_contents().get_data()) == 0):
                # if the reader has no apparent data, then I need to OCR it before I can do anything with the text
                # will want to pipe out the text directly, rather than ocr the pdf then try to get the text with pypdf
                pass

    # pdf = PDF_Metadata(metadata.title, metadata.author, metadata.creation_date)
    # Currently I don't think I actually need this, but I'm going to leave this here in case I need it late
    
    # Most of these papers will have more than one author; if there are 3 or more, I want to change it to first author et al.
    authors = metadata.author


    new_title = "{authors} {metadata.creation_date} {metadata.title}"
    print(new_title)

    

    