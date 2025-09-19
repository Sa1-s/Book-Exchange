import streamlit as st
import book_db as db
import time

st.set_page_config(page_title="Christ Uni Textbook Exchange", page_icon="!", layout="centered")

st.markdown("""
    <link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=PT+Serif:ital,wght@0,400;0,700;1,400;1,700&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)

with open('static/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.title("! Christ University Textbook Exchange")
st.write("A platform for students to buy and sell used textbooks within the Christ community.")

st.header("List Your Textbook for Sale")
with st.form("new_book_form", clear_on_submit=True):
    st.subheader("Book Details")
    title = st.text_input("Book Title")
    author = st.text_input("Author")
    department = st.selectbox("Department", ["BCA", "BBA", "Psychology", "Law", "Engineering"])
    semester = st.number_input("Semester", min_value=1, max_value=8, step=1)
    price = st.number_input("Selling Price (₹)", min_value=0)
    
    st.subheader("Your Contact Information")
    seller_name = st.text_input("Your Name")
    seller_contact = st.text_input("Your Email (e.g., name.surname@christuniversity.in)")

    submitted = st.form_submit_button("List My Book")

    if submitted:
        if not all([title, author, department, semester, price, seller_name, seller_contact]):
            st.error("Please fill out all fields before submitting.")
        else:
            new_book = {
                "id": int(time.time()), 
                "title": title,
                "author": author,
                "department": department,
                "semester": semester,
                "price": price,
                "seller_name": seller_name,
                "seller_contact": seller_contact
            }

            current_books = db.load_books()
            current_books.append(new_book)
            db.save_books(current_books)
            st.success(f"Success! Your book '{title}' has been listed.")

st.header("Find a Textbook")

all_books = db.load_books()
search_query = st.text_input("Search by Title or Author")
dept_filter = st.selectbox("Filter by Department", ["All"] + sorted(list(set(b['department'] for b in all_books))))

sort_key = st.selectbox("Sort by", ["Price (Low to High)", "Price (High to Low)"])

filtered_books = all_books
if search_query:
    filtered_books = [b for b in filtered_books if search_query.lower() in b['title'].lower() or search_query.lower() in b['author'].lower()]
if dept_filter != "All":
    filtered_books = [b for b in filtered_books if b['department'] == dept_filter]


if sort_key == "Price (Low to High)":
    sorted_books = sorted(filtered_books, key=lambda x: x['price'])
else:
    sorted_books = sorted(filtered_books, key=lambda x: x['price'], reverse=True)


if not sorted_books:
    st.info("No books found. Try adjusting your filters or be the first to list one!")
else:
    for book in sorted_books:
        with st.container():
            st.subheader(book['title'])
            st.text(f"Author: {book['author']}")
            st.text(f"Department: {book['department']} | Semester: {book['semester']}")
            st.markdown(f"**Price: ₹{book['price']}**")
            st.markdown(f"Contact Seller: `{book['seller_contact']}`")
            
            if st.button("Find Related Books", key=f"rec_{book['id']}"):
                recommendations = db.recommend_related_books(book, all_books)
                if recommendations:
                    st.write("**You might also be interested in:**")
                    for rec in recommendations[:2]:
                        st.success(f"- {rec['title']} (Dept: {rec['department']}) for ₹{rec['price']}")
                else:
                    st.write("No other related books found in this department.")
            st.divider()