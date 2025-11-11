from collections import defaultdict
import typing
from bs4 import BeautifulSoup
import pandas as pd
from streamlit.runtime.uploaded_file_manager import UploadedFile


class Instagram:
    def get_from_json(self):
        ...

    def get_from_html(self, html_file: UploadedFile) -> typing.Dict[str, str]:
        """
        Extracts user information from an HTML file.
        This method parses the provided HTML file to extract user names and their corresponding links.
        It searches for anchor tags within the main section of the HTML document and stores the text
        and href attributes in a dictionary.
        Args:
            html_file (UploadedFile): A file-like object containing the HTML content to be parsed.
        Returns:
            typing.Dict[str, str]: A dictionary where the keys are user names (text of the anchor tags)
            and the values are the corresponding href links.
        """

        users_dict = defaultdict(str)
        soup = BeautifulSoup(html_file.read(), "html.parser")
        main_divs = soup.find("main", attrs={"role": "main"})
        if main_divs:
            for link in main_divs.find_all("a"):
                users_dict[link.text] = link["href"]
        return users_dict
    
    def get_users_from_file(self, file: UploadedFile):
        """
        Extracts user data from an uploaded file based on its format.
        Args:
            file (UploadedFile): The uploaded file containing user data. 
                                 Supported formats are HTML and JSON.
        Returns:
            list: A list of users extracted from the file.
        Raises:
            NotImplementedError: If the file format is not supported.
        """

        if file.name.endswith(".html"):
            users = self.get_from_html(file)
        elif file.name.endswith(".json"):
            users = self.get_from_json(file)
        else:
            raise NotImplementedError
        return users
    def get_users_df(self, user_object: dict) -> pd.DataFrame:
        """
        Converts a dictionary of user data into a pandas DataFrame with formatted links.
        Args:
            user_object (dict): A dictionary where keys are user names and values are URLs.
        Returns:
            pd.DataFrame: A DataFrame with two columns:
                - "Name": The user names from the dictionary keys.
                - "Link": The URLs from the dictionary values, formatted as clickable HTML links.
        """

        df = pd.DataFrame(list(user_object.items()), columns=["Name", "Link"])
        df["Link"] = df["Link"].apply(
            lambda x: f'<a href="{x}" target="_blank">Click Here</a>'
        )
        return df
    
    def master(self, followers_file: UploadedFile, following_file: UploadedFile) -> pd.DataFrame:
        """
        Identifies users who are being followed but do not follow back.
        Args:
            followers_file (UploadedFile): A file containing the list of followers.
            following_file (UploadedFile): A file containing the list of users being followed.
        Returns:
            pd.DataFrame: A DataFrame containing the users who do not follow back, 
                          along with their associated details.
        """

        followers = self.get_users_from_file(followers_file)
        followings = self.get_users_from_file(following_file)
        followers_user = followers.keys()
        not_following_users = {}
        for following in followings.keys():
            if following.split("/")[-1] not in followers_user:
                not_following_users[following.split("/")[-1]] = followings[following]
        
        return self.get_users_df(not_following_users)



        
