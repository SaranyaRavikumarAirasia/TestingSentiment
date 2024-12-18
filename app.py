import streamlit as st
import sidebar
import textPage
import imdbReviewsPage
import imagePage

# You can add more pages here when you implement them
# import audioPage
# import videoPage
# import twitterAnalysisPage

# Show the sidebar and get the selected page
page = sidebar.show()

# Render the selected page
if page == "Text":
    textPage.renderPage()
elif page == "IMDb movie reviews":
    imdbReviewsPage.renderPage()
elif page == "Image":
    imagePage.renderPage()
# Uncomment and implement the following pages if needed
# elif page == "Audio":
#     audioPage.renderPage()
# elif page == "Video":
#     videoPage.main()
# elif page == "Twitter Data":
#     twitterAnalysisPage.renderPage()
