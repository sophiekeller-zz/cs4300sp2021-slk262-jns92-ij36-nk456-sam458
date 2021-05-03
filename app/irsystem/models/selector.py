from sklearn.decomposition import TruncatedSVD
from scipy.sparse import csr_matrix
from sklearn import datasets
import numpy as np
import pickle

def select_n_components(var_ratio, goal_var: float) -> int:
      # Set initial variance explained so far
      total_variance = 0.0
      
      # Set initial number of features
      n_components = 0
      
      # For the explained variance of each feature:
      for explained_variance in var_ratio:
          
          # Add the explained variance to the total
          total_variance += explained_variance
          
          # Add one to the number of components
          n_components += 1
          
          # If we reach our goal level of explained variance
          if total_variance >= goal_var:
              # End the loop
              break
              
      # Return the number of components
      return n_components

for city in ["london","amsterdam", "barcelona", "berlin", "dubai"]:
  for category in ["accommodation", "restaurant", "attraction"]:
    X = pickle.load(open(f"pickle/vec-array-{city}-{category}.pickle", "rb"))

    print("actual", X.T.shape[1])
    # Make sparse matrix
    X_sparse = csr_matrix(X)

    # Create and run an TSVD with one less than number of features
    tsvd = TruncatedSVD(n_components=X_sparse.shape[1]-1)
    X_tsvd = tsvd.fit(X)

    # List of explained variances
    tsvd_var_ratios = tsvd.explained_variance_ratio_

    n_components = select_n_components(tsvd_var_ratios, 0.95)
    svd = TruncatedSVD(n_components=n_components, n_iter=7, random_state=42)
    print(f"selected {n_components} out of {X.T.shape[1]} for {city}-{category}")
    svd.fit(X.T)
    #pickle.dump(svd.transform(X.T), open(f"pickle/svd-dict-{city}-{category}.pickle", "wb"))
    pickle.dump(svd.inverse_transform(svd.transform(X.T)), open(f"pickle/svd-obj-{city}-{category}.pickle", "wb"))