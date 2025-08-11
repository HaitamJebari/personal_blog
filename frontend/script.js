// Personal Blog System JavaScript

class BlogSystem {
    constructor() {
        this.posts = [];
        this.categories = [];
        this.comments = [];
        this.currentPage = 1;
        this.postsPerPage = 6;
        this.filteredPosts = [];
        this.currentPost = null;
        
        this.init();
    }

    init() {
        this.loadSampleData();
        this.setupEventListeners();
        this.updateStats();
        this.showSection('home');
        this.renderPosts();
        this.renderCategories();
        this.renderSidebar();
    }

    setupEventListeners() {
        // Search functionality
        document.getElementById('searchInput').addEventListener('input', (e) => {
            this.searchPosts(e.target.value);
        });

        // Sort functionality
        document.getElementById('sortSelect').addEventListener('change', () => {
            this.sortPosts();
        });

        // Form submissions
        document.getElementById('postForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.savePost();
        });

        document.getElementById('commentForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.saveComment();
        });

        document.getElementById('contactForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.sendContactMessage();
        });

        // Enter key for search
        document.getElementById('searchInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.searchPosts(e.target.value);
            }
        });
    }

    loadSampleData() {
        // Sample blog posts
        this.posts = [
            {
                id: 1,
                title: "Getting Started with Modern JavaScript",
                excerpt: "Learn the fundamentals of ES6+ JavaScript features and how they can improve your development workflow.",
                content: `
                    <p>JavaScript has evolved significantly over the years, and modern JavaScript (ES6+) brings many powerful features that make development more efficient and enjoyable.</p>
                    
                    <h3>Key ES6+ Features</h3>
                    <ul>
                        <li><strong>Arrow Functions:</strong> Concise syntax for writing functions</li>
                        <li><strong>Template Literals:</strong> String interpolation and multi-line strings</li>
                        <li><strong>Destructuring:</strong> Extract values from arrays and objects</li>
                        <li><strong>Modules:</strong> Import and export functionality</li>
                        <li><strong>Promises & Async/Await:</strong> Better asynchronous programming</li>
                    </ul>
                    
                    <h3>Arrow Functions Example</h3>
                    <pre><code>// Traditional function
function add(a, b) {
    return a + b;
}

// Arrow function
const add = (a, b) => a + b;</code></pre>
                    
                    <p>These modern features help write cleaner, more maintainable code and are essential for any JavaScript developer today.</p>
                `,
                category: "programming",
                tags: ["javascript", "es6", "programming", "tutorial"],
                author: "John Developer",
                date: "2025-01-15",
                image: "https://images.unsplash.com/photo-1627398242454-45a1465c2479?w=600&h=300&fit=crop",
                featured: true,
                comments: 12,
                views: 1250
            },
            {
                id: 2,
                title: "Building Responsive Web Applications",
                excerpt: "Master the art of creating web applications that work seamlessly across all devices and screen sizes.",
                content: `
                    <p>Responsive web design is no longer optional—it's essential. With users accessing websites from various devices, creating responsive applications ensures the best user experience.</p>
                    
                    <h3>Key Principles</h3>
                    <ol>
                        <li><strong>Mobile-First Approach:</strong> Start designing for mobile devices</li>
                        <li><strong>Flexible Grid Systems:</strong> Use CSS Grid and Flexbox</li>
                        <li><strong>Responsive Images:</strong> Optimize images for different screen sizes</li>
                        <li><strong>Touch-Friendly Interface:</strong> Design for touch interactions</li>
                    </ol>
                    
                    <h3>CSS Grid Example</h3>
                    <pre><code>.container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1rem;
}</code></pre>
                    
                    <p>By following these principles, you can create applications that provide excellent user experiences across all devices.</p>
                `,
                category: "web-development",
                tags: ["responsive", "css", "mobile", "design"],
                author: "John Developer",
                date: "2025-01-10",
                image: "https://images.unsplash.com/photo-1559028006-448665bd7c7f?w=600&h=300&fit=crop",
                featured: false,
                comments: 8,
                views: 890
            },
            {
                id: 3,
                title: "Introduction to Python for Web Development",
                excerpt: "Discover how Python can be used for web development with frameworks like Flask and Django.",
                content: `
                    <p>Python has become one of the most popular languages for web development, thanks to its simplicity and powerful frameworks.</p>
                    
                    <h3>Popular Python Web Frameworks</h3>
                    <ul>
                        <li><strong>Django:</strong> Full-featured framework for large applications</li>
                        <li><strong>Flask:</strong> Lightweight and flexible micro-framework</li>
                        <li><strong>FastAPI:</strong> Modern framework for building APIs</li>
                    </ul>
                    
                    <h3>Simple Flask Example</h3>
                    <pre><code>from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)</code></pre>
                    
                    <p>Python's readable syntax and extensive ecosystem make it an excellent choice for web development projects.</p>
                `,
                category: "programming",
                tags: ["python", "flask", "django", "backend"],
                author: "John Developer",
                date: "2025-01-05",
                image: "https://images.unsplash.com/photo-1526379095098-d400fd0bf935?w=600&h=300&fit=crop",
                featured: false,
                comments: 15,
                views: 1100
            },
            {
                id: 4,
                title: "Database Design Best Practices",
                excerpt: "Learn essential principles for designing efficient and scalable database schemas.",
                content: `
                    <p>Good database design is crucial for application performance and maintainability. Here are key principles to follow.</p>
                    
                    <h3>Normalization</h3>
                    <p>Organize data to reduce redundancy and improve data integrity:</p>
                    <ul>
                        <li>First Normal Form (1NF): Eliminate repeating groups</li>
                        <li>Second Normal Form (2NF): Remove partial dependencies</li>
                        <li>Third Normal Form (3NF): Remove transitive dependencies</li>
                    </ul>
                    
                    <h3>Indexing Strategy</h3>
                    <pre><code>-- Create index for frequently queried columns
CREATE INDEX idx_user_email ON users(email);
CREATE INDEX idx_post_date ON posts(created_at);</code></pre>
                    
                    <p>Proper database design ensures your application can scale and perform well as data grows.</p>
                `,
                category: "technology",
                tags: ["database", "sql", "design", "performance"],
                author: "John Developer",
                date: "2025-01-01",
                image: "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=600&h=300&fit=crop",
                featured: false,
                comments: 6,
                views: 750
            },
            {
                id: 5,
                title: "Version Control with Git: Advanced Tips",
                excerpt: "Master advanced Git techniques to improve your development workflow and collaboration.",
                content: `
                    <p>Git is an essential tool for developers. Beyond basic commands, advanced techniques can significantly improve your workflow.</p>
                    
                    <h3>Useful Git Commands</h3>
                    <pre><code># Interactive rebase to clean up commits
git rebase -i HEAD~3

# Stash changes with a message
git stash push -m "Work in progress on feature X"

# Cherry-pick specific commits
git cherry-pick abc123def456</code></pre>
                    
                    <h3>Branching Strategies</h3>
                    <ul>
                        <li><strong>Git Flow:</strong> Feature branches, develop, and master</li>
                        <li><strong>GitHub Flow:</strong> Simple feature branch workflow</li>
                        <li><strong>GitLab Flow:</strong> Environment-based branching</li>
                    </ul>
                    
                    <p>Mastering these techniques will make you a more effective developer and team member.</p>
                `,
                category: "tutorials",
                tags: ["git", "version-control", "workflow", "collaboration"],
                author: "John Developer",
                date: "2024-12-28",
                image: "https://images.unsplash.com/photo-1556075798-4825dfaaf498?w=600&h=300&fit=crop",
                featured: false,
                comments: 9,
                views: 920
            },
            {
                id: 6,
                title: "The Future of Web Development",
                excerpt: "Explore emerging trends and technologies that will shape the future of web development.",
                content: `
                    <p>Web development continues to evolve rapidly. Here are the trends and technologies shaping its future.</p>
                    
                    <h3>Emerging Technologies</h3>
                    <ul>
                        <li><strong>WebAssembly:</strong> Near-native performance in browsers</li>
                        <li><strong>Progressive Web Apps:</strong> App-like experiences on the web</li>
                        <li><strong>Serverless Architecture:</strong> Function-as-a-Service computing</li>
                        <li><strong>AI Integration:</strong> Machine learning in web applications</li>
                    </ul>
                    
                    <h3>Development Trends</h3>
                    <blockquote>
                        "The future of web development lies in creating more immersive, performant, and accessible experiences for users across all devices and platforms."
                    </blockquote>
                    
                    <p>Staying updated with these trends will help you build better applications and advance your career.</p>
                `,
                category: "technology",
                tags: ["future", "trends", "webassembly", "pwa"],
                author: "John Developer",
                date: "2024-12-25",
                image: "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=600&h=300&fit=crop",
                featured: true,
                comments: 18,
                views: 1500
            }
        ];

        // Sample categories
        this.categories = [
            {
                id: 'programming',
                name: 'Programming',
                description: 'Programming languages, frameworks, and development techniques',
                image: 'https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=400&h=300&fit=crop',
                count: this.posts.filter(p => p.category === 'programming').length
            },
            {
                id: 'web-development',
                name: 'Web Development',
                description: 'Frontend and backend web development topics',
                image: 'https://images.unsplash.com/photo-1547658719-da2b51169166?w=400&h=300&fit=crop',
                count: this.posts.filter(p => p.category === 'web-development').length
            },
            {
                id: 'technology',
                name: 'Technology',
                description: 'Latest technology trends and innovations',
                image: 'https://images.unsplash.com/photo-1518709268805-4e9042af2176?w=400&h=300&fit=crop',
                count: this.posts.filter(p => p.category === 'technology').length
            },
            {
                id: 'tutorials',
                name: 'Tutorials',
                description: 'Step-by-step guides and how-to articles',
                image: 'https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=400&h=300&fit=crop',
                count: this.posts.filter(p => p.category === 'tutorials').length
            }
        ];

        // Sample comments
        this.comments = [
            {
                id: 1,
                postId: 1,
                author: "Alice Johnson",
                email: "alice@example.com",
                content: "Great article! The arrow function examples really helped me understand the concept better.",
                date: "2025-01-16",
                approved: true
            },
            {
                id: 2,
                postId: 1,
                author: "Bob Smith",
                email: "bob@example.com",
                content: "Thanks for the clear explanations. Looking forward to more JavaScript tutorials!",
                date: "2025-01-17",
                approved: true
            },
            {
                id: 3,
                postId: 2,
                author: "Carol Davis",
                email: "carol@example.com",
                content: "The CSS Grid example is exactly what I needed for my current project.",
                date: "2025-01-11",
                approved: true
            }
        ];

        this.filteredPosts = [...this.posts];
    }

    updateStats() {
        document.getElementById('totalPosts').textContent = this.posts.length;
        document.getElementById('totalCategories').textContent = this.categories.length;
        document.getElementById('totalComments').textContent = this.comments.filter(c => c.approved).length;
    }

    searchPosts(query = '') {
        const searchTerm = query.toLowerCase().trim();
        
        if (!searchTerm) {
            this.filteredPosts = [...this.posts];
        } else {
            this.filteredPosts = this.posts.filter(post =>
                post.title.toLowerCase().includes(searchTerm) ||
                post.excerpt.toLowerCase().includes(searchTerm) ||
                post.content.toLowerCase().includes(searchTerm) ||
                post.tags.some(tag => tag.toLowerCase().includes(searchTerm)) ||
                post.category.toLowerCase().includes(searchTerm)
            );
        }

        this.currentPage = 1;
        this.renderPosts();
    }

    sortPosts() {
        const sortBy = document.getElementById('sortSelect').value;
        
        switch (sortBy) {
            case 'date-desc':
                this.filteredPosts.sort((a, b) => new Date(b.date) - new Date(a.date));
                break;
            case 'date-asc':
                this.filteredPosts.sort((a, b) => new Date(a.date) - new Date(b.date));
                break;
            case 'title':
                this.filteredPosts.sort((a, b) => a.title.localeCompare(b.title));
                break;
            case 'comments':
                this.filteredPosts.sort((a, b) => b.comments - a.comments);
                break;
        }

        this.renderPosts();
    }

    filterByCategory(categoryId) {
        if (categoryId === 'all') {
            this.filteredPosts = [...this.posts];
        } else {
            this.filteredPosts = this.posts.filter(post => post.category === categoryId);
        }
        
        this.currentPage = 1;
        this.renderPosts();
        this.showSection('home');
    }

    renderPosts() {
        const startIndex = (this.currentPage - 1) * this.postsPerPage;
        const endIndex = startIndex + this.postsPerPage;
        const postsToShow = this.filteredPosts.slice(startIndex, endIndex);

        // Render featured post
        const featuredPost = this.posts.find(p => p.featured);
        if (featuredPost) {
            document.getElementById('featuredPost').innerHTML = this.renderFeaturedPost(featuredPost);
        }

        // Render posts grid
        const container = document.getElementById('postsContainer');
        
        if (postsToShow.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-search"></i>
                    <h5>No posts found</h5>
                    <p>Try adjusting your search terms or browse by category</p>
                </div>
            `;
            this.renderPagination();
            return;
        }

        container.innerHTML = postsToShow.map(post => this.renderPostCard(post)).join('');
        this.renderPagination();
    }

    renderFeaturedPost(post) {
        return `
            <div class="card featured-post">
                <div class="row g-0">
                    <div class="col-md-6">
                        <img src="${post.image}" alt="${post.title}" class="img-fluid h-100 w-100" style="object-fit: cover;">
                    </div>
                    <div class="col-md-6">
                        <div class="card-body h-100 d-flex flex-column">
                            <div class="featured-badge">Featured Post</div>
                            <h3 class="card-title">${post.title}</h3>
                            <div class="post-meta mb-3">
                                <i class="fas fa-user"></i> ${post.author}
                                <i class="fas fa-calendar ms-3"></i> ${this.formatDate(post.date)}
                                <i class="fas fa-folder ms-3"></i> ${this.getCategoryName(post.category)}
                            </div>
                            <p class="card-text flex-grow-1">${post.excerpt}</p>
                            <div class="post-tags mb-3">
                                ${post.tags.map(tag => `<span class="post-tag">${tag}</span>`).join('')}
                            </div>
                            <div class="d-flex justify-content-between align-items-center">
                                <a href="#" class="read-more" onclick="blogSystem.showPost(${post.id})">Read More <i class="fas fa-arrow-right"></i></a>
                                <div class="text-muted">
                                    <i class="fas fa-comments"></i> ${post.comments}
                                    <i class="fas fa-eye ms-2"></i> ${post.views}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    renderPostCard(post) {
        return `
            <div class="col-md-6 mb-4">
                <div class="card post-card h-100" onclick="blogSystem.showPost(${post.id})">
                    <img src="${post.image}" alt="${post.title}" class="post-image">
                    <div class="card-body d-flex flex-column">
                        <div class="post-meta">
                            <i class="fas fa-user"></i> ${post.author}
                            <i class="fas fa-calendar ms-3"></i> ${this.formatDate(post.date)}
                            <i class="fas fa-folder ms-3"></i> ${this.getCategoryName(post.category)}
                        </div>
                        <h5 class="post-title">${post.title}</h5>
                        <p class="post-excerpt flex-grow-1">${post.excerpt}</p>
                        <div class="post-tags mb-3">
                            ${post.tags.slice(0, 3).map(tag => `<span class="post-tag">${tag}</span>`).join('')}
                        </div>
                        <div class="d-flex justify-content-between align-items-center">
                            <a href="#" class="read-more" onclick="event.stopPropagation(); blogSystem.showPost(${post.id})">Read More</a>
                            <div class="text-muted">
                                <i class="fas fa-comments"></i> ${post.comments}
                                <i class="fas fa-eye ms-2"></i> ${post.views}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    renderPagination() {
        const totalPages = Math.ceil(this.filteredPosts.length / this.postsPerPage);
        const pagination = document.getElementById('pagination');

        if (totalPages <= 1) {
            pagination.innerHTML = '';
            return;
        }

        let paginationHTML = '';

        // Previous button
        paginationHTML += `
            <li class="page-item ${this.currentPage === 1 ? 'disabled' : ''}">
                <a class="page-link" href="#" onclick="blogSystem.goToPage(${this.currentPage - 1})">Previous</a>
            </li>
        `;

        // Page numbers
        for (let i = 1; i <= totalPages; i++) {
            if (i === 1 || i === totalPages || (i >= this.currentPage - 2 && i <= this.currentPage + 2)) {
                paginationHTML += `
                    <li class="page-item ${i === this.currentPage ? 'active' : ''}">
                        <a class="page-link" href="#" onclick="blogSystem.goToPage(${i})">${i}</a>
                    </li>
                `;
            } else if (i === this.currentPage - 3 || i === this.currentPage + 3) {
                paginationHTML += '<li class="page-item disabled"><span class="page-link">...</span></li>';
            }
        }

        // Next button
        paginationHTML += `
            <li class="page-item ${this.currentPage === totalPages ? 'disabled' : ''}">
                <a class="page-link" href="#" onclick="blogSystem.goToPage(${this.currentPage + 1})">Next</a>
            </li>
        `;

        pagination.innerHTML = paginationHTML;
    }

    goToPage(page) {
        const totalPages = Math.ceil(this.filteredPosts.length / this.postsPerPage);
        if (page >= 1 && page <= totalPages) {
            this.currentPage = page;
            this.renderPosts();
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    }

    showPost(postId) {
        const post = this.posts.find(p => p.id === postId);
        if (!post) return;

        this.currentPost = post;
        
        // Increment views
        post.views++;

        // Render post content
        document.getElementById('postContent').innerHTML = `
            <header class="mb-4">
                <h1 class="display-5 fw-bold">${post.title}</h1>
                <div class="post-meta mb-3">
                    <i class="fas fa-user"></i> ${post.author}
                    <i class="fas fa-calendar ms-3"></i> ${this.formatDate(post.date)}
                    <i class="fas fa-folder ms-3"></i> ${this.getCategoryName(post.category)}
                    <i class="fas fa-eye ms-3"></i> ${post.views} views
                </div>
                <div class="post-tags mb-4">
                    ${post.tags.map(tag => `<span class="post-tag">${tag}</span>`).join('')}
                </div>
            </header>
            <img src="${post.image}" alt="${post.title}" class="img-fluid mb-4 rounded">
            <div class="post-content">
                ${post.content}
            </div>
        `;

        // Set post ID for comments
        document.getElementById('postId').value = postId;

        // Render comments
        this.renderComments(postId);

        // Render related posts
        this.renderRelatedPosts(post);

        this.showSection('postDetail');
    }

    renderComments(postId) {
        const postComments = this.comments.filter(c => c.postId === postId && c.approved);
        
        document.getElementById('commentsCount').textContent = `(${postComments.length})`;

        const container = document.getElementById('commentsList');
        
        if (postComments.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-comments"></i>
                    <h6>No comments yet</h6>
                    <p>Be the first to leave a comment!</p>
                </div>
            `;
            return;
        }

        container.innerHTML = postComments.map(comment => `
            <div class="comment">
                <div class="comment-header">
                    <span class="comment-author">${comment.author}</span>
                    <span class="comment-date ms-auto">${this.formatDate(comment.date)}</span>
                </div>
                <div class="comment-content">${comment.content}</div>
                <div class="comment-actions">
                    <a href="#" onclick="blogSystem.replyToComment(${comment.id})">Reply</a>
                    <a href="#" onclick="blogSystem.likeComment(${comment.id})">Like</a>
                </div>
            </div>
        `).join('');
    }

    renderRelatedPosts(currentPost) {
        const related = this.posts
            .filter(p => p.id !== currentPost.id && p.category === currentPost.category)
            .slice(0, 3);

        const container = document.getElementById('relatedPosts');
        
        if (related.length === 0) {
            container.innerHTML = '<p class="text-muted">No related posts found.</p>';
            return;
        }

        container.innerHTML = related.map(post => `
            <div class="mb-3">
                <a href="#" onclick="blogSystem.showPost(${post.id})" class="text-decoration-none">
                    <div class="row g-2">
                        <div class="col-4">
                            <img src="${post.image}" alt="${post.title}" class="img-fluid rounded" style="height: 60px; object-fit: cover;">
                        </div>
                        <div class="col-8">
                            <h6 class="mb-1 text-truncate">${post.title}</h6>
                            <small class="text-muted">${this.formatDate(post.date)}</small>
                        </div>
                    </div>
                </a>
            </div>
        `).join('');
    }

    renderCategories() {
        const grid = document.getElementById('categoriesGrid');
        grid.innerHTML = this.categories.map(category => `
            <div class="col-lg-3 col-md-6 mb-4">
                <a href="#" class="category-card" onclick="blogSystem.filterByCategory('${category.id}')">
                    <div class="card h-100">
                        <img src="${category.image}" alt="${category.name}" class="category-image">
                        <div class="category-info">
                            <h5 class="category-title">${category.name}</h5>
                            <p class="category-count">${category.count} posts</p>
                            <p class="text-muted">${category.description}</p>
                        </div>
                    </div>
                </a>
            </div>
        `).join('');
    }

    renderSidebar() {
        // Render categories list
        const categoriesList = document.getElementById('categoriesList');
        categoriesList.innerHTML = `
            <ul class="widget-list">
                <li><a href="#" onclick="blogSystem.filterByCategory('all')">All Categories <span class="widget-count">${this.posts.length}</span></a></li>
                ${this.categories.map(cat => `
                    <li><a href="#" onclick="blogSystem.filterByCategory('${cat.id}')">${cat.name} <span class="widget-count">${cat.count}</span></a></li>
                `).join('')}
            </ul>
        `;

        // Render recent comments
        const recentComments = document.getElementById('recentComments');
        const latestComments = this.comments.filter(c => c.approved).slice(0, 3);
        
        if (latestComments.length === 0) {
            recentComments.innerHTML = '<p class="text-muted">No comments yet.</p>';
        } else {
            recentComments.innerHTML = latestComments.map(comment => {
                const post = this.posts.find(p => p.id === comment.postId);
                return `
                    <div class="recent-comment">
                        <div class="recent-comment-author">${comment.author}</div>
                        <div class="recent-comment-post">on "${post ? post.title : 'Unknown Post'}"</div>
                        <div class="recent-comment-excerpt">${comment.content.substring(0, 80)}...</div>
                    </div>
                `;
            }).join('');
        }

        // Render tag cloud
        const tagCloud = document.getElementById('tagCloud');
        const allTags = this.posts.flatMap(post => post.tags);
        const tagCounts = {};
        allTags.forEach(tag => {
            tagCounts[tag] = (tagCounts[tag] || 0) + 1;
        });
        
        const popularTags = Object.entries(tagCounts)
            .sort(([,a], [,b]) => b - a)
            .slice(0, 10);

        tagCloud.innerHTML = `
            <div class="tag-cloud">
                ${popularTags.map(([tag, count]) => `
                    <span class="post-tag" onclick="blogSystem.searchPosts('${tag}')" style="cursor: pointer;">${tag}</span>
                `).join('')}
            </div>
        `;
    }

    savePost() {
        const form = document.getElementById('postForm');
        const formData = new FormData(form);
        
        const postData = {
            id: document.getElementById('editPostId').value || Date.now(),
            title: document.getElementById('postTitle').value,
            excerpt: document.getElementById('postExcerpt').value,
            content: document.getElementById('postContentInput').value.replace(/\n/g, '<br>'),
            category: document.getElementById('postCategory').value,
            tags: document.getElementById('postTags').value.split(',').map(tag => tag.trim()).filter(tag => tag),
            image: document.getElementById('postImage').value || 'https://images.unsplash.com/photo-1486312338219-ce68d2c6f44d?w=600&h=300&fit=crop',
            featured: document.getElementById('postFeatured').checked,
            author: "John Developer",
            date: new Date().toISOString().split('T')[0],
            comments: 0,
            views: 0
        };

        const existingIndex = this.posts.findIndex(p => p.id == postData.id);
        
        if (existingIndex >= 0) {
            this.posts[existingIndex] = { ...this.posts[existingIndex], ...postData };
            this.showAlert('Post updated successfully!', 'success');
        } else {
            this.posts.unshift(postData);
            this.showAlert('Post published successfully!', 'success');
        }

        this.filteredPosts = [...this.posts];
        this.updateStats();
        this.renderPosts();
        this.renderSidebar();
        this.resetPostForm();
        this.renderPostsManagement();
    }

    saveComment() {
        const postId = parseInt(document.getElementById('postId').value);
        const name = document.getElementById('commentName').value;
        const email = document.getElementById('commentEmail').value;
        const content = document.getElementById('commentContent').value;

        const comment = {
            id: Date.now(),
            postId: postId,
            author: name,
            email: email,
            content: content,
            date: new Date().toISOString().split('T')[0],
            approved: true
        };

        this.comments.push(comment);
        
        // Update post comment count
        const post = this.posts.find(p => p.id === postId);
        if (post) {
            post.comments++;
        }

        this.renderComments(postId);
        this.renderSidebar();
        this.updateStats();
        
        // Reset form
        document.getElementById('commentForm').reset();
        
        this.showAlert('Comment posted successfully!', 'success');
    }

    sendContactMessage() {
        const name = document.getElementById('contactName').value;
        const email = document.getElementById('contactEmail').value;
        const subject = document.getElementById('contactSubject').value;
        const message = document.getElementById('contactMessage').value;

        // In a real application, this would send the message to a server
        console.log('Contact message:', { name, email, subject, message });
        
        this.showAlert('Message sent successfully! We\'ll get back to you soon.', 'success');
        document.getElementById('contactForm').reset();
    }

    resetPostForm() {
        document.getElementById('postForm').reset();
        document.getElementById('editPostId').value = '';
    }

    editPost(postId) {
        const post = this.posts.find(p => p.id === postId);
        if (!post) return;

        document.getElementById('editPostId').value = post.id;
        document.getElementById('postTitle').value = post.title;
        document.getElementById('postExcerpt').value = post.excerpt;
        document.getElementById('postContent').value = post.content.replace(/<br>/g, '\n');
        document.getElementById('postCategory').value = post.category;
        document.getElementById('postTags').value = post.tags.join(', ');
        document.getElementById('postImage').value = post.image;
        document.getElementById('postFeatured').checked = post.featured;

        // Switch to new post tab
        const newPostTab = document.querySelector('[data-bs-toggle="tab"][href="#newPost"]');
        const tab = new bootstrap.Tab(newPostTab);
        tab.show();
    }

    deletePost(postId) {
        if (confirm('Are you sure you want to delete this post?')) {
            this.posts = this.posts.filter(p => p.id !== postId);
            this.filteredPosts = [...this.posts];
            this.comments = this.comments.filter(c => c.postId !== postId);
            
            this.updateStats();
            this.renderPosts();
            this.renderSidebar();
            this.renderPostsManagement();
            
            this.showAlert('Post deleted successfully!', 'success');
        }
    }

    renderPostsManagement() {
        const container = document.getElementById('postsManagement');
        
        if (this.posts.length === 0) {
            container.innerHTML = '<p class="text-muted">No posts found.</p>';
            return;
        }

        container.innerHTML = this.posts.map(post => `
            <div class="admin-post-item">
                <div class="admin-post-title">${post.title}</div>
                <div class="admin-post-meta">
                    Category: ${this.getCategoryName(post.category)} | 
                    Date: ${this.formatDate(post.date)} | 
                    Comments: ${post.comments} | 
                    Views: ${post.views}
                    ${post.featured ? ' | <span class="badge bg-warning">Featured</span>' : ''}
                </div>
                <div class="admin-post-actions">
                    <button class="btn btn-sm btn-primary" onclick="blogSystem.editPost(${post.id})">Edit</button>
                    <button class="btn btn-sm btn-info" onclick="blogSystem.showPost(${post.id})">View</button>
                    <button class="btn btn-sm btn-danger" onclick="blogSystem.deletePost(${post.id})">Delete</button>
                </div>
            </div>
        `).join('');
    }

    renderCommentsManagement() {
        const container = document.getElementById('commentsManagement');
        
        if (this.comments.length === 0) {
            container.innerHTML = '<p class="text-muted">No comments found.</p>';
            return;
        }

        container.innerHTML = this.comments.map(comment => {
            const post = this.posts.find(p => p.id === comment.postId);
            return `
                <div class="admin-post-item">
                    <div class="admin-post-title">${comment.author} - ${comment.email}</div>
                    <div class="admin-post-meta">
                        Post: "${post ? post.title : 'Unknown'}" | 
                        Date: ${this.formatDate(comment.date)} | 
                        Status: ${comment.approved ? '<span class="badge bg-success">Approved</span>' : '<span class="badge bg-warning">Pending</span>'}
                    </div>
                    <div class="mb-2">${comment.content}</div>
                    <div class="admin-post-actions">
                        ${!comment.approved ? `<button class="btn btn-sm btn-success" onclick="blogSystem.approveComment(${comment.id})">Approve</button>` : ''}
                        <button class="btn btn-sm btn-danger" onclick="blogSystem.deleteComment(${comment.id})">Delete</button>
                    </div>
                </div>
            `;
        }).join('');
    }

    approveComment(commentId) {
        const comment = this.comments.find(c => c.id === commentId);
        if (comment) {
            comment.approved = true;
            this.renderCommentsManagement();
            this.renderSidebar();
            this.updateStats();
            this.showAlert('Comment approved!', 'success');
        }
    }

    deleteComment(commentId) {
        if (confirm('Are you sure you want to delete this comment?')) {
            const comment = this.comments.find(c => c.id === commentId);
            if (comment) {
                // Update post comment count
                const post = this.posts.find(p => p.id === comment.postId);
                if (post && post.comments > 0) {
                    post.comments--;
                }
            }
            
            this.comments = this.comments.filter(c => c.id !== commentId);
            this.renderCommentsManagement();
            this.renderSidebar();
            this.updateStats();
            this.showAlert('Comment deleted!', 'success');
        }
    }

    showSection(sectionId) {
        // Hide all sections
        document.querySelectorAll('.content-section').forEach(section => {
            section.style.display = 'none';
        });

        // Show selected section
        document.getElementById(sectionId).style.display = 'block';

        // Update navigation
        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.remove('active');
        });

        const activeLink = document.querySelector(`[onclick*="showSection('${sectionId}')"]`);
        if (activeLink) {
            activeLink.classList.add('active');
        }

        // Load section-specific content
        if (sectionId === 'admin') {
            this.renderPostsManagement();
            this.renderCommentsManagement();
        }
    }

    getCategoryName(categoryId) {
        const category = this.categories.find(c => c.id === categoryId);
        return category ? category.name : categoryId;
    }

    formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', { 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric' 
        });
    }

    showAlert(message, type = 'info') {
        // Remove existing alerts
        const existingAlert = document.querySelector('.alert');
        if (existingAlert) {
            existingAlert.remove();
        }

        const alert = document.createElement('div');
        alert.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        alert.style.cssText = 'top: 80px; right: 20px; z-index: 9999; min-width: 300px;';
        alert.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        document.body.appendChild(alert);

        // Auto-dismiss after 3 seconds
        setTimeout(() => {
            if (alert.parentNode) {
                alert.remove();
            }
        }, 3000);
    }

    // Placeholder methods for future implementation
    replyToComment(commentId) {
        this.showAlert('Reply functionality coming soon!', 'info');
    }

    likeComment(commentId) {
        this.showAlert('Like functionality coming soon!', 'info');
    }
}

// Global functions for HTML onclick events
function showSection(sectionId) {
    blogSystem.showSection(sectionId);
}

function searchPosts() {
    const query = document.getElementById('searchInput').value;
    blogSystem.searchPosts(query);
}

// Initialize the blog system when the page loads
let blogSystem;
document.addEventListener('DOMContentLoaded', () => {
    blogSystem = new BlogSystem();
});

