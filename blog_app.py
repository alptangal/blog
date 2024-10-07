import streamlit as st
import sqlite3
from datetime import datetime
import pandas as pd

# Khởi tạo database
def init_db():
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS posts
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
         title TEXT NOT NULL,
         content TEXT NOT NULL,
         author TEXT NOT NULL,
         created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
    ''')
    conn.commit()
    conn.close()

# Hàm thêm bài viết mới
def add_post(title, content, author):
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    c.execute('INSERT INTO posts (title, content, author) VALUES (?, ?, ?)',
              (title, content, author))
    conn.commit()
    conn.close()

# Hàm lấy tất cả bài viết
def get_all_posts():
    conn = sqlite3.connect('blog.db')
    posts = pd.read_sql_query('SELECT * FROM posts ORDER BY created_at DESC', conn)
    conn.close()
    return posts

# Hàm lấy một bài viết theo ID
def get_post_by_id(post_id):
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    c.execute('SELECT * FROM posts WHERE id = ?', (post_id,))
    post = c.fetchone()
    conn.close()
    return post

# Hàm cập nhật bài viết
def update_post(post_id, title, content):
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    c.execute('UPDATE posts SET title = ?, content = ? WHERE id = ?',
              (title, content, post_id))
    conn.commit()
    conn.close()

# Hàm xóa bài viết
def delete_post(post_id):
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    c.execute('DELETE FROM posts WHERE id = ?', (post_id,))
    conn.commit()
    conn.close()

# Khởi tạo ứng dụng
def main():
    st.title('Blog Application')
    init_db()

    # Sidebar menu
    menu = st.sidebar.selectbox(
        'Menu',
        ['Home', 'Create Post', 'Edit/Delete Post']
    )

    if menu == 'Home':
        st.subheader('Recent Blog Posts')
        posts = get_all_posts()
        for _, post in posts.iterrows():
            st.write(f"## {post['title']}")
            st.write(f"*By {post['author']} on {post['created_at']}*")
            st.write(post['content'])
            st.write('---')

    elif menu == 'Create Post':
        st.subheader('Create New Post')
        title = st.text_input('Post Title')
        content = st.text_area('Post Content')
        author = st.text_input('Author Name')
        if st.button('Create Post'):
            if title and content and author:
                add_post(title, content, author)
                st.success('Post created successfully!')
            else:
                st.error('All fields are required!')

    elif menu == 'Edit/Delete Post':
        st.subheader('Edit/Delete Post')
        posts = get_all_posts()
        post_to_edit = st.selectbox('Select post to edit/delete',
                                   posts['id'].tolist(),
                                   format_func=lambda x: posts.loc[posts['id'] == x, 'title'].iloc[0])
        
        if post_to_edit:
            post = get_post_by_id(post_to_edit)
            if post:
                title = st.text_input('Edit Title', value=post[1])
                content = st.text_area('Edit Content', value=post[2])
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button('Update Post'):
                        update_post(post_to_edit, title, content)
                        st.success('Post updated successfully!')
                
                with col2:
                    if st.button('Delete Post'):
                        delete_post(post_to_edit)
                        st.success('Post deleted successfully!')

if __name__ == '__main__':
    main()