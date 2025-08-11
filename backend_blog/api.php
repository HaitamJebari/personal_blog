<?php
/**
 * Personal Blog System - PHP Backend API
 * Provides RESTful API endpoints for blog management
 */

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, Authorization');

// Handle preflight requests
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}

class BlogAPI {
    private $postsFile;
    private $categoriesFile;
    private $commentsFile;
    private $settingsFile;
    
    public function __construct() {
        $this->postsFile = __DIR__ . '/../database/posts.json';
        $this->categoriesFile = __DIR__ . '/../database/categories.json';
        $this->commentsFile = __DIR__ . '/../database/comments.json';
        $this->settingsFile = __DIR__ . '/../database/settings.json';
        $this->ensureDataFiles();
    }
    
    private function ensureDataFiles() {
        $dir = dirname($this->postsFile);
        if (!is_dir($dir)) {
            mkdir($dir, 0755, true);
        }
        
        if (!file_exists($this->postsFile)) {
            $this->initializePosts();
        }
        
        if (!file_exists($this->categoriesFile)) {
            $this->initializeCategories();
        }
        
        if (!file_exists($this->commentsFile)) {
            file_put_contents($this->commentsFile, json_encode([]));
        }
        
        if (!file_exists($this->settingsFile)) {
            $this->initializeSettings();
        }
    }
    
    private function initializePosts() {
        $posts = [
            [
                'id' => 1,
                'title' => 'Getting Started with Modern JavaScript',
                'slug' => 'getting-started-modern-javascript',
                'excerpt' => 'Learn the fundamentals of ES6+ JavaScript features and how they can improve your development workflow.',
                'content' => 'JavaScript has evolved significantly over the years, and modern JavaScript (ES6+) brings many powerful features that make development more efficient and enjoyable...',
                'category' => 'programming',
                'tags' => ['javascript', 'es6', 'programming', 'tutorial'],
                'author' => 'John Developer',
                'authorEmail' => 'john@example.com',
                'date' => date('Y-m-d', strtotime('-5 days')),
                'image' => 'https://images.unsplash.com/photo-1627398242454-45a1465c2479?w=600&h=300&fit=crop',
                'featured' => true,
                'published' => true,
                'comments' => 12,
                'views' => 1250,
                'likes' => 89,
                'metaTitle' => 'Getting Started with Modern JavaScript - TechBlog',
                'metaDescription' => 'Learn ES6+ JavaScript features including arrow functions, template literals, destructuring, and more.',
                'createdAt' => date('c', strtotime('-5 days')),
                'updatedAt' => date('c', strtotime('-1 day'))
            ],
            [
                'id' => 2,
                'title' => 'Building Responsive Web Applications',
                'slug' => 'building-responsive-web-applications',
                'excerpt' => 'Master the art of creating web applications that work seamlessly across all devices and screen sizes.',
                'content' => 'Responsive web design is no longer optional—it\'s essential. With users accessing websites from various devices, creating responsive applications ensures the best user experience...',
                'category' => 'web-development',
                'tags' => ['responsive', 'css', 'mobile', 'design'],
                'author' => 'John Developer',
                'authorEmail' => 'john@example.com',
                'date' => date('Y-m-d', strtotime('-10 days')),
                'image' => 'https://images.unsplash.com/photo-1559028006-448665bd7c7f?w=600&h=300&fit=crop',
                'featured' => false,
                'published' => true,
                'comments' => 8,
                'views' => 890,
                'likes' => 67,
                'metaTitle' => 'Building Responsive Web Applications - TechBlog',
                'metaDescription' => 'Learn how to create responsive web applications using CSS Grid, Flexbox, and mobile-first design principles.',
                'createdAt' => date('c', strtotime('-10 days')),
                'updatedAt' => date('c', strtotime('-3 days'))
            ]
        ];
        
        file_put_contents($this->postsFile, json_encode($posts, JSON_PRETTY_PRINT));
    }
    
    private function initializeCategories() {
        $categories = [
            [
                'id' => 'programming',
                'name' => 'Programming',
                'slug' => 'programming',
                'description' => 'Programming languages, frameworks, and development techniques',
                'image' => 'https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=400&h=300&fit=crop',
                'color' => '#3498db',
                'active' => true,
                'createdAt' => date('c'),
                'updatedAt' => date('c')
            ],
            [
                'id' => 'web-development',
                'name' => 'Web Development',
                'slug' => 'web-development',
                'description' => 'Frontend and backend web development topics',
                'image' => 'https://images.unsplash.com/photo-1547658719-da2b51169166?w=400&h=300&fit=crop',
                'color' => '#e74c3c',
                'active' => true,
                'createdAt' => date('c'),
                'updatedAt' => date('c')
            ],
            [
                'id' => 'technology',
                'name' => 'Technology',
                'slug' => 'technology',
                'description' => 'Latest technology trends and innovations',
                'image' => 'https://images.unsplash.com/photo-1518709268805-4e9042af2176?w=400&h=300&fit=crop',
                'color' => '#27ae60',
                'active' => true,
                'createdAt' => date('c'),
                'updatedAt' => date('c')
            ],
            [
                'id' => 'tutorials',
                'name' => 'Tutorials',
                'slug' => 'tutorials',
                'description' => 'Step-by-step guides and how-to articles',
                'image' => 'https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=400&h=300&fit=crop',
                'color' => '#f39c12',
                'active' => true,
                'createdAt' => date('c'),
                'updatedAt' => date('c')
            ]
        ];
        
        file_put_contents($this->categoriesFile, json_encode($categories, JSON_PRETTY_PRINT));
    }
    
    private function initializeSettings() {
        $settings = [
            'siteName' => 'TechBlog',
            'siteDescription' => 'Exploring technology, sharing knowledge, and building the future',
            'siteUrl' => 'https://techblog.example.com',
            'authorName' => 'John Developer',
            'authorEmail' => 'john@example.com',
            'authorBio' => 'Full-stack developer passionate about web technologies and sharing knowledge.',
            'postsPerPage' => 10,
            'commentsEnabled' => true,
            'moderateComments' => true,
            'allowGuestComments' => true,
            'socialLinks' => [
                'twitter' => 'https://twitter.com/johndeveloper',
                'github' => 'https://github.com/johndeveloper',
                'linkedin' => 'https://linkedin.com/in/johndeveloper'
            ],
            'analytics' => [
                'googleAnalytics' => '',
                'facebookPixel' => ''
            ],
            'seo' => [
                'metaTitle' => 'TechBlog - Technology and Programming Blog',
                'metaDescription' => 'Explore the latest in technology, programming tutorials, and web development insights.',
                'metaKeywords' => 'technology, programming, web development, tutorials, javascript, php, python'
            ],
            'createdAt' => date('c'),
            'updatedAt' => date('c')
        ];
        
        file_put_contents($this->settingsFile, json_encode($settings, JSON_PRETTY_PRINT));
    }
    
    private function loadData($file) {
        if (!file_exists($file)) {
            return [];
        }
        $data = file_get_contents($file);
        return json_decode($data, true) ?: [];
    }
    
    private function saveData($file, $data) {
        return file_put_contents($file, json_encode($data, JSON_PRETTY_PRINT));
    }
    
    private function generateId() {
        return time() . rand(1000, 9999);
    }
    
    private function generateSlug($title) {
        $slug = strtolower(trim($title));
        $slug = preg_replace('/[^a-z0-9-]/', '-', $slug);
        $slug = preg_replace('/-+/', '-', $slug);
        return trim($slug, '-');
    }
    
    // Post methods
    public function getAllPosts($filters = []) {
        $posts = $this->loadData($this->postsFile);
        
        // Filter published posts only for public access
        if (!isset($filters['admin']) || !$filters['admin']) {
            $posts = array_filter($posts, function($post) {
                return $post['published'] ?? true;
            });
        }
        
        // Apply filters
        if (!empty($filters['category'])) {
            $posts = array_filter($posts, function($post) use ($filters) {
                return $post['category'] === $filters['category'];
            });
        }
        
        if (!empty($filters['tag'])) {
            $posts = array_filter($posts, function($post) use ($filters) {
                return in_array($filters['tag'], $post['tags'] ?? []);
            });
        }
        
        if (!empty($filters['search'])) {
            $searchTerm = strtolower($filters['search']);
            $posts = array_filter($posts, function($post) use ($searchTerm) {
                return strpos(strtolower($post['title']), $searchTerm) !== false ||
                       strpos(strtolower($post['excerpt']), $searchTerm) !== false ||
                       strpos(strtolower($post['content']), $searchTerm) !== false ||
                       (isset($post['tags']) && array_intersect($post['tags'], [$searchTerm]));
            });
        }
        
        if (isset($filters['featured']) && $filters['featured']) {
            $posts = array_filter($posts, function($post) {
                return $post['featured'] ?? false;
            });
        }
        
        // Sort posts
        $sortBy = $filters['sort'] ?? 'date-desc';
        switch ($sortBy) {
            case 'date-asc':
                usort($posts, function($a, $b) {
                    return strtotime($a['date']) - strtotime($b['date']);
                });
                break;
            case 'title':
                usort($posts, function($a, $b) {
                    return strcmp($a['title'], $b['title']);
                });
                break;
            case 'views':
                usort($posts, function($a, $b) {
                    return ($b['views'] ?? 0) - ($a['views'] ?? 0);
                });
                break;
            case 'comments':
                usort($posts, function($a, $b) {
                    return ($b['comments'] ?? 0) - ($a['comments'] ?? 0);
                });
                break;
            default: // date-desc
                usort($posts, function($a, $b) {
                    return strtotime($b['date']) - strtotime($a['date']);
                });
                break;
        }
        
        // Pagination
        $page = intval($filters['page'] ?? 1);
        $limit = intval($filters['limit'] ?? 10);
        $offset = ($page - 1) * $limit;
        
        $totalPosts = count($posts);
        $paginatedPosts = array_slice($posts, $offset, $limit);
        
        return [
            'success' => true,
            'data' => array_values($paginatedPosts),
            'pagination' => [
                'page' => $page,
                'limit' => $limit,
                'total' => $totalPosts,
                'pages' => ceil($totalPosts / $limit)
            ]
        ];
    }
    
    public function getPost($identifier) {
        $posts = $this->loadData($this->postsFile);
        
        foreach ($posts as &$post) {
            if ($post['id'] == $identifier || $post['slug'] === $identifier) {
                // Increment views
                $post['views'] = ($post['views'] ?? 0) + 1;
                $this->saveData($this->postsFile, $posts);
                
                return [
                    'success' => true,
                    'data' => $post
                ];
            }
        }
        
        return [
            'success' => false,
            'message' => 'Post not found'
        ];
    }
    
    public function createPost($data) {
        $errors = $this->validatePost($data);
        if (!empty($errors)) {
            return [
                'success' => false,
                'message' => 'Validation failed',
                'errors' => $errors
            ];
        }
        
        $posts = $this->loadData($this->postsFile);
        
        $post = [
            'id' => intval($this->generateId()),
            'title' => trim($data['title']),
            'slug' => $this->generateSlug($data['title']),
            'excerpt' => trim($data['excerpt'] ?? ''),
            'content' => trim($data['content']),
            'category' => $data['category'],
            'tags' => $data['tags'] ?? [],
            'author' => $data['author'] ?? 'Anonymous',
            'authorEmail' => $data['authorEmail'] ?? '',
            'date' => date('Y-m-d'),
            'image' => $data['image'] ?? '',
            'featured' => boolval($data['featured'] ?? false),
            'published' => boolval($data['published'] ?? true),
            'comments' => 0,
            'views' => 0,
            'likes' => 0,
            'metaTitle' => $data['metaTitle'] ?? $data['title'],
            'metaDescription' => $data['metaDescription'] ?? $data['excerpt'] ?? '',
            'createdAt' => date('c'),
            'updatedAt' => date('c')
        ];
        
        // Ensure unique slug
        $originalSlug = $post['slug'];
        $counter = 1;
        while ($this->slugExists($post['slug'], $posts)) {
            $post['slug'] = $originalSlug . '-' . $counter;
            $counter++;
        }
        
        $posts[] = $post;
        
        if ($this->saveData($this->postsFile, $posts)) {
            return [
                'success' => true,
                'message' => 'Post created successfully',
                'data' => $post
            ];
        }
        
        return [
            'success' => false,
            'message' => 'Failed to save post'
        ];
    }
    
    public function updatePost($id, $data) {
        $errors = $this->validatePost($data);
        if (!empty($errors)) {
            return [
                'success' => false,
                'message' => 'Validation failed',
                'errors' => $errors
            ];
        }
        
        $posts = $this->loadData($this->postsFile);
        
        for ($i = 0; $i < count($posts); $i++) {
            if ($posts[$i]['id'] == $id) {
                $oldSlug = $posts[$i]['slug'];
                $newSlug = $this->generateSlug($data['title']);
                
                // Ensure unique slug if title changed
                if ($newSlug !== $oldSlug) {
                    $originalSlug = $newSlug;
                    $counter = 1;
                    while ($this->slugExists($newSlug, $posts, $id)) {
                        $newSlug = $originalSlug . '-' . $counter;
                        $counter++;
                    }
                }
                
                $posts[$i]['title'] = trim($data['title']);
                $posts[$i]['slug'] = $newSlug;
                $posts[$i]['excerpt'] = trim($data['excerpt'] ?? $posts[$i]['excerpt']);
                $posts[$i]['content'] = trim($data['content']);
                $posts[$i]['category'] = $data['category'];
                $posts[$i]['tags'] = $data['tags'] ?? $posts[$i]['tags'];
                $posts[$i]['image'] = $data['image'] ?? $posts[$i]['image'];
                $posts[$i]['featured'] = boolval($data['featured'] ?? $posts[$i]['featured']);
                $posts[$i]['published'] = boolval($data['published'] ?? $posts[$i]['published']);
                $posts[$i]['metaTitle'] = $data['metaTitle'] ?? $data['title'];
                $posts[$i]['metaDescription'] = $data['metaDescription'] ?? $data['excerpt'] ?? $posts[$i]['metaDescription'];
                $posts[$i]['updatedAt'] = date('c');
                
                if ($this->saveData($this->postsFile, $posts)) {
                    return [
                        'success' => true,
                        'message' => 'Post updated successfully',
                        'data' => $posts[$i]
                    ];
                }
                
                return [
                    'success' => false,
                    'message' => 'Failed to save post'
                ];
            }
        }
        
        return [
            'success' => false,
            'message' => 'Post not found'
        ];
    }
    
    public function deletePost($id) {
        $posts = $this->loadData($this->postsFile);
        $originalCount = count($posts);
        
        $posts = array_filter($posts, function($post) use ($id) {
            return $post['id'] != $id;
        });
        
        if (count($posts) < $originalCount) {
            // Also delete related comments
            $comments = $this->loadData($this->commentsFile);
            $comments = array_filter($comments, function($comment) use ($id) {
                return $comment['postId'] != $id;
            });
            $this->saveData($this->commentsFile, array_values($comments));
            
            if ($this->saveData($this->postsFile, array_values($posts))) {
                return [
                    'success' => true,
                    'message' => 'Post deleted successfully'
                ];
            }
            
            return [
                'success' => false,
                'message' => 'Failed to delete post'
            ];
        }
        
        return [
            'success' => false,
            'message' => 'Post not found'
        ];
    }
    
    private function slugExists($slug, $posts, $excludeId = null) {
        foreach ($posts as $post) {
            if ($post['slug'] === $slug && ($excludeId === null || $post['id'] != $excludeId)) {
                return true;
            }
        }
        return false;
    }
    
    private function validatePost($data) {
        $errors = [];
        
        if (empty($data['title'])) {
            $errors[] = 'Post title is required';
        }
        
        if (empty($data['content'])) {
            $errors[] = 'Post content is required';
        }
        
        if (empty($data['category'])) {
            $errors[] = 'Post category is required';
        }
        
        return $errors;
    }
    
    // Comment methods
    public function getAllComments($filters = []) {
        $comments = $this->loadData($this->commentsFile);
        
        // Filter by post ID
        if (!empty($filters['postId'])) {
            $comments = array_filter($comments, function($comment) use ($filters) {
                return $comment['postId'] == $filters['postId'];
            });
        }
        
        // Filter by approval status
        if (isset($filters['approved'])) {
            $approved = boolval($filters['approved']);
            $comments = array_filter($comments, function($comment) use ($approved) {
                return ($comment['approved'] ?? false) === $approved;
            });
        }
        
        // Sort by date (newest first)
        usort($comments, function($a, $b) {
            return strtotime($b['date']) - strtotime($a['date']);
        });
        
        return [
            'success' => true,
            'data' => array_values($comments)
        ];
    }
    
    public function createComment($data) {
        $errors = $this->validateComment($data);
        if (!empty($errors)) {
            return [
                'success' => false,
                'message' => 'Validation failed',
                'errors' => $errors
            ];
        }
        
        $comments = $this->loadData($this->commentsFile);
        $settings = $this->loadData($this->settingsFile);
        
        $comment = [
            'id' => intval($this->generateId()),
            'postId' => intval($data['postId']),
            'author' => trim($data['author']),
            'email' => trim($data['email']),
            'website' => trim($data['website'] ?? ''),
            'content' => trim($data['content']),
            'date' => date('Y-m-d H:i:s'),
            'approved' => !($settings['moderateComments'] ?? true),
            'ip' => $_SERVER['REMOTE_ADDR'] ?? '',
            'userAgent' => $_SERVER['HTTP_USER_AGENT'] ?? '',
            'createdAt' => date('c'),
            'updatedAt' => date('c')
        ];
        
        $comments[] = $comment;
        
        if ($this->saveData($this->commentsFile, $comments)) {
            // Update post comment count if approved
            if ($comment['approved']) {
                $this->updatePostCommentCount($comment['postId'], 1);
            }
            
            return [
                'success' => true,
                'message' => $comment['approved'] ? 'Comment posted successfully' : 'Comment submitted for moderation',
                'data' => $comment
            ];
        }
        
        return [
            'success' => false,
            'message' => 'Failed to save comment'
        ];
    }
    
    public function approveComment($id) {
        $comments = $this->loadData($this->commentsFile);
        
        for ($i = 0; $i < count($comments); $i++) {
            if ($comments[$i]['id'] == $id) {
                if (!$comments[$i]['approved']) {
                    $comments[$i]['approved'] = true;
                    $comments[$i]['updatedAt'] = date('c');
                    
                    if ($this->saveData($this->commentsFile, $comments)) {
                        $this->updatePostCommentCount($comments[$i]['postId'], 1);
                        
                        return [
                            'success' => true,
                            'message' => 'Comment approved successfully'
                        ];
                    }
                }
                
                return [
                    'success' => false,
                    'message' => 'Comment is already approved'
                ];
            }
        }
        
        return [
            'success' => false,
            'message' => 'Comment not found'
        ];
    }
    
    public function deleteComment($id) {
        $comments = $this->loadData($this->commentsFile);
        $originalCount = count($comments);
        
        $deletedComment = null;
        foreach ($comments as $comment) {
            if ($comment['id'] == $id) {
                $deletedComment = $comment;
                break;
            }
        }
        
        $comments = array_filter($comments, function($comment) use ($id) {
            return $comment['id'] != $id;
        });
        
        if (count($comments) < $originalCount) {
            if ($this->saveData($this->commentsFile, array_values($comments))) {
                // Update post comment count if comment was approved
                if ($deletedComment && $deletedComment['approved']) {
                    $this->updatePostCommentCount($deletedComment['postId'], -1);
                }
                
                return [
                    'success' => true,
                    'message' => 'Comment deleted successfully'
                ];
            }
            
            return [
                'success' => false,
                'message' => 'Failed to delete comment'
            ];
        }
        
        return [
            'success' => false,
            'message' => 'Comment not found'
        ];
    }
    
    private function updatePostCommentCount($postId, $increment) {
        $posts = $this->loadData($this->postsFile);
        
        for ($i = 0; $i < count($posts); $i++) {
            if ($posts[$i]['id'] == $postId) {
                $posts[$i]['comments'] = max(0, ($posts[$i]['comments'] ?? 0) + $increment);
                $this->saveData($this->postsFile, $posts);
                break;
            }
        }
    }
    
    private function validateComment($data) {
        $errors = [];
        
        if (empty($data['postId'])) {
            $errors[] = 'Post ID is required';
        }
        
        if (empty($data['author'])) {
            $errors[] = 'Author name is required';
        }
        
        if (empty($data['email']) || !filter_var($data['email'], FILTER_VALIDATE_EMAIL)) {
            $errors[] = 'Valid email is required';
        }
        
        if (empty($data['content'])) {
            $errors[] = 'Comment content is required';
        }
        
        return $errors;
    }
    
    // Category methods
    public function getAllCategories() {
        $categories = $this->loadData($this->categoriesFile);
        $posts = $this->loadData($this->postsFile);
        
        // Add post count to each category
        foreach ($categories as &$category) {
            $category['count'] = count(array_filter($posts, function($post) use ($category) {
                return $post['category'] === $category['id'] && ($post['published'] ?? true);
            }));
        }
        
        return [
            'success' => true,
            'data' => $categories
        ];
    }
    
    // Analytics methods
    public function getAnalytics() {
        $posts = $this->loadData($this->postsFile);
        $comments = $this->loadData($this->commentsFile);
        
        $totalPosts = count($posts);
        $publishedPosts = count(array_filter($posts, function($post) {
            return $post['published'] ?? true;
        }));
        $totalComments = count(array_filter($comments, function($comment) {
            return $comment['approved'] ?? false;
        }));
        $totalViews = array_sum(array_column($posts, 'views'));
        $totalLikes = array_sum(array_column($posts, 'likes'));
        
        // Category stats
        $categoryStats = [];
        foreach ($posts as $post) {
            $category = $post['category'];
            if (!isset($categoryStats[$category])) {
                $categoryStats[$category] = [
                    'posts' => 0,
                    'views' => 0,
                    'comments' => 0
                ];
            }
            $categoryStats[$category]['posts']++;
            $categoryStats[$category]['views'] += $post['views'] ?? 0;
            $categoryStats[$category]['comments'] += $post['comments'] ?? 0;
        }
        
        // Popular posts
        $popularPosts = $posts;
        usort($popularPosts, function($a, $b) {
            return ($b['views'] ?? 0) - ($a['views'] ?? 0);
        });
        $popularPosts = array_slice($popularPosts, 0, 5);
        
        // Recent activity
        $recentComments = $comments;
        usort($recentComments, function($a, $b) {
            return strtotime($b['date']) - strtotime($a['date']);
        });
        $recentComments = array_slice($recentComments, 0, 10);
        
        return [
            'success' => true,
            'data' => [
                'totalPosts' => $totalPosts,
                'publishedPosts' => $publishedPosts,
                'totalComments' => $totalComments,
                'totalViews' => $totalViews,
                'totalLikes' => $totalLikes,
                'categoryStats' => $categoryStats,
                'popularPosts' => $popularPosts,
                'recentComments' => $recentComments
            ]
        ];
    }
    
    // Settings methods
    public function getSettings() {
        $settings = $this->loadData($this->settingsFile);
        
        return [
            'success' => true,
            'data' => $settings
        ];
    }
    
    public function updateSettings($data) {
        $settings = $this->loadData($this->settingsFile);
        
        // Update settings
        foreach ($data as $key => $value) {
            $settings[$key] = $value;
        }
        
        $settings['updatedAt'] = date('c');
        
        if ($this->saveData($this->settingsFile, $settings)) {
            return [
                'success' => true,
                'message' => 'Settings updated successfully',
                'data' => $settings
            ];
        }
        
        return [
            'success' => false,
            'message' => 'Failed to update settings'
        ];
    }
}

// Initialize API
$api = new BlogAPI();

// Get request method and parse URL
$method = $_SERVER['REQUEST_METHOD'];
$path = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
$pathParts = explode('/', trim($path, '/'));

// Get the endpoint
$endpoint = end($pathParts);

// Get request data
$input = json_decode(file_get_contents('php://input'), true);
$queryParams = $_GET;

try {
    switch ($method) {
        case 'GET':
            if ($endpoint === 'posts' || $endpoint === 'api.php') {
                $response = $api->getAllPosts($queryParams);
            } elseif ($endpoint === 'categories') {
                $response = $api->getAllCategories();
            } elseif ($endpoint === 'comments') {
                $response = $api->getAllComments($queryParams);
            } elseif ($endpoint === 'analytics') {
                $response = $api->getAnalytics();
            } elseif ($endpoint === 'settings') {
                $response = $api->getSettings();
            } elseif (isset($queryParams['id']) || isset($queryParams['slug'])) {
                $identifier = $queryParams['id'] ?? $queryParams['slug'];
                $response = $api->getPost($identifier);
            } else {
                $response = $api->getAllPosts($queryParams);
            }
            break;
            
        case 'POST':
            if ($endpoint === 'posts') {
                $response = $api->createPost($input);
            } elseif ($endpoint === 'comments') {
                $response = $api->createComment($input);
            } else {
                $response = [
                    'success' => false,
                    'message' => 'Invalid endpoint for POST request'
                ];
            }
            break;
            
        case 'PUT':
            if ($endpoint === 'posts' && isset($queryParams['id'])) {
                $response = $api->updatePost($queryParams['id'], $input);
            } elseif ($endpoint === 'comments' && isset($queryParams['id']) && isset($queryParams['action']) && $queryParams['action'] === 'approve') {
                $response = $api->approveComment($queryParams['id']);
            } elseif ($endpoint === 'settings') {
                $response = $api->updateSettings($input);
            } else {
                $response = [
                    'success' => false,
                    'message' => 'Invalid endpoint or missing parameters for PUT request'
                ];
            }
            break;
            
        case 'DELETE':
            if ($endpoint === 'posts' && isset($queryParams['id'])) {
                $response = $api->deletePost($queryParams['id']);
            } elseif ($endpoint === 'comments' && isset($queryParams['id'])) {
                $response = $api->deleteComment($queryParams['id']);
            } else {
                $response = [
                    'success' => false,
                    'message' => 'ID is required for deletion'
                ];
            }
            break;
            
        default:
            $response = [
                'success' => false,
                'message' => 'Method not allowed'
            ];
            http_response_code(405);
            break;
    }
} catch (Exception $e) {
    $response = [
        'success' => false,
        'message' => 'Server error: ' . $e->getMessage()
    ];
    http_response_code(500);
}

// Send response
echo json_encode($response, JSON_PRETTY_PRINT);
?>

