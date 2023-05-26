import streamlit
import snowflake.connector
import pandas

# Set the title of the Streamlit application
streamlit.title("Zena's Amazing Athleisure Catalog")

# Connect to Snowflake using the credentials stored in Streamlit secrets
my_cnx = snowflake.connector.connect(**streamlit.secrets.snowflake)

# Create a cursor to execute SQL queries
my_cur = my_cnx.cursor()

# Fetch the available colors or styles from the catalog_for_website table
my_cur.execute("select color_or_style from catalog_for_website")
my_catalog = my_cur.fetchall()

# Create a DataFrame from the fetched data
df = pandas.DataFrame(my_catalog)

# Convert the color_or_style column to a list
color_list = df[0].values.tolist()

# Display a selectbox in the Streamlit app to pick a sweatsuit color or style
option = streamlit.selectbox('Pick a sweatsuit color or style:', list(color_list))

# Generate the product caption based on the selected option
product_caption = 'Our warm, comfortable, ' + option + ' sweatsuit!'

# Fetch the details of the selected product from the catalog_for_website table
my_cur.execute("select direct_url, price, size_list, upsell_product_desc from catalog_for_website where color_or_style = '" + option + "';")
df2 = my_cur.fetchone()

# Display the image of the product with a caption
streamlit.image(df2[0], width=400, caption=product_caption)

# Display the price, sizes available, and upsell product description
streamlit.write('Price: ', df2[1])
streamlit.write('Sizes Available: ', df2[2])
streamlit.write(df2[3])
