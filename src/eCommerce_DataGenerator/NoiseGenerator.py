import numpy as np

class NoiseGenerator:
    def __init__(self, n_customers):
    ##TODO: Sometimes magnitude needs to be a fraction, would be better in these instances to rename
        self.n_customers = n_customers

    def add_gaussian_noise(self,df, col_name, noise_min, noise_max):
        return df[col_name] + np.random.normal(noise_min, noise_max, size=self.n_customers)

    def add_errors(df, col_name, magnitude, ):

        if not (0 <= magnitude <= 1):
            raise ValueError("Magnitude must be a fraction between 0 and 1.")
        
        errors = df[col_name].copy()
        n_errors = int(magnitude * len(errors))
        error_indices = np.random.choice(df.index, size=n_errors, replace=False)

        if df[col_name].dtype == 'int' and set(df[col_name].unique()) == {0, 1}:
            errors[error_indices] = 1 - errors[error_indices]
        else:
            raise ValueError("This function currently only supports binary (0/1) columns.")
        
        return errors

    def add_missing_values(df, col_name, magnitude):

        if not (0 <= magnitude <= 1):
            raise ValueError("Magnitude must be a fraction between 0 and 1.")
        
        df.loc[df.sample(frac=magnitude).index, col_name] = np.nan
        return df[col_name]

    def introduce_bias(df, pred_col, inf_col, threshold, magnitude):
        if not (df[inf_col].min() <= threshold <= df[inf_col].max()):
            raise ValueError(f"Threshold {threshold} is out of bounds for column {inf_col}.")
        
        errors = df[pred_col].copy()
        errors[df[inf_col] > threshold] += magnitude

        return errors
    
    def add_outliers(df, col_name, magnitude, size_multiplier):
        ##TODO:Add something that calculates the magnitude automatically?
        if not (0 <= size_multiplier <= 1):
            raise ValueError("Size multiplier must be a fraction between 0 and 1.")
        
        outlier_indices = np.random.choice(df.index, size=int(size_multiplier * len(df)), replace=False)
        errors = df[col_name].copy() 
        errors.loc[outlier_indices] *= magnitude

        return errors

    def error_treatment_assignment(df, col_name, treatment_error_rate):
        treatment_errors = df[col_name].copy()
        treatment_error_indices = np.random.choice(df.index, size=int(treatment_error_rate * len(treatment_errors)), replace=False)
        treatment_errors[treatment_error_indices] = 1 - treatment_errors[treatment_error_indices]

        return treatment_errors