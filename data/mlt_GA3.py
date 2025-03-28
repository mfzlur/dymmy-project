MLT_GA3 = [
    {
        "text": "What is the main goal of clustering algorithms",
        "options": ["To predict a continuous output", "To predict a categorical output", "To group similar data points together", "To reduce the dimensionality of the data"],
        "correct_answer": 2
    },
    {
        "text": "Which of the following is an example of a clustering algorithm",
        "options": ["Linear Regression", "Decision Tree", "k-means", "Support Vector Machine"],
        "correct_answer": 2
    },
    {
        "text": "What is the core idea behind the k-means clustering algorithm",
        "options": ["To find the best linear separator", "To partition data into k clusters, minimizing the within-cluster variance", "To find the shortest path between data points", "To create a hierarchy of clusters"],
        "correct_answer": 1
    },
    {
        "text": "In Lloyds algorithm (k-means), what happens in the assignment step",
        "options": ["Cluster centroids are initialized", "Each data point is assigned to the nearest centroid", "The number of clusters k is determined", "The algorithm terminates"],
        "correct_answer": 1
    },
    {
        "text": "What is the condition for convergence in the k-means algorithm",
        "options": ["When the cluster assignments no longer change", "After a fixed number of iterations", "When the algorithm reaches a predefined accuracy", "When the data points are perfectly separated"],
        "correct_answer": 0
    },
    {
        "text": "Why might k-means fail to converge",
        "options": ["Because the data is too simple", "Due to poor initialization or oscillations", "Because the data is perfectly clustered already", "If k is too large"],
        "correct_answer": 1
    },
    {
        "text": "What is the typical shape of clusters produced by the k-means algorithm",
        "options": ["Arbitrary shapes", "Complex, non-convex shapes", "Convex, roughly spherical shapes", "Hierarchical structures"],
        "correct_answer": 2
    },
    {
        "text": "What kind of data distributions does k-means struggle with",
        "options": ["Uniform distributions", "Gaussian distributions", "Linearly separable data", "Non-convex or elongated clusters"],
        "correct_answer": 3
    },
    {
        "text": "What is the primary advantage of k-means++ over standard k-means initialization",
        "options": ["k-means++ is faster", "k-means++ is guaranteed to find the optimal clustering", "k-means++ selects initial centroids that are more spread out", "k-means++ requires less memory"],
        "correct_answer": 2
    },
    {
        "text": "How does k-means++ improve centroid initialization",
        "options": ["By randomly selecting centroids", "By selecting the densest data points", "By iteratively selecting centroids, giving preference to points far from existing centroids", "By using a hierarchical clustering approach"],
        "correct_answer": 3
    },
    {
        "text": "What is the elbow method commonly used for in k-means clustering",
        "options": ["To determine the optimal learning rate", "To determine the optimal number of clusters k", "To visualize the cluster assignments", "To reduce the dimensionality of the data"],
        "correct_answer": 1
    },
    {
        "text": "What does the silhouette score measure in the context of clustering",
        "options": ["The distance between data points", "The quality of cluster assignments", "The number of iterations required for convergence", "The size of the clusters"],
        "correct_answer": 1
    }
]
