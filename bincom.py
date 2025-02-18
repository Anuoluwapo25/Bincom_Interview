import random
import statistics
from collections import Counter
# import psycopg2
from typing import List

class ColorAnalyzer:
    def __init__(self, colors: List[str]):
        self.colors = colors
        self.color_counts = Counter(colors)
    
    def get_mean_color(self) -> str:
        """Question 1: Which color of shirt is the mean color?"""
        mean_freq = statistics.mean(self.color_counts.values())
        return min(self.color_counts.items(), 
                  key=lambda x: abs(x[1] - mean_freq))[0]
    
    def get_most_worn_color(self) -> str:
        """Question 2: Which color is mostly worn throughout the week?"""
        return self.color_counts.most_common(1)[0][0]
    
    def get_median_color(self) -> str:
        """Question 3: Which color is the median?"""
        sorted_colors = sorted(self.color_counts.items(), key=lambda x: x[1])
        return sorted_colors[len(sorted_colors)//2][0]
    
    def get_color_variance(self) -> float:
        """Question 4: Get the variance of the colors"""
        return statistics.variance(self.color_counts.values())
    
    def get_red_probability(self) -> float:
        """Question 5: Probability that a randomly chosen color is red"""
        red_count = self.color_counts.get('RED', 0)
        return red_count / len(self.colors) if self.colors else 0

    def save_to_postgresql(self, db_params: dict):
        """Question 6: Save the colours and their frequencies in postgresql database"""
        try:
            conn = psycopg2.connect(**db_params)
            cur = conn.cursor()
            
            cur.execute("""
                CREATE TABLE IF NOT EXISTS color_frequencies (
                    color VARCHAR(50) PRIMARY KEY,
                    frequency INTEGER
                )
            """)
            

            for color, freq in self.color_counts.items():
                cur.execute("""
                    INSERT INTO color_frequencies (color, frequency)
                    VALUES (%s, %s)
                    ON CONFLICT (color) DO UPDATE SET frequency = EXCLUDED.frequency
                """, (color, freq))
            
            conn.commit()
            cur.close()
            conn.close()
            print("Successfully saved to database")
        except Exception as e:
            print(f"Database error: {e}")

def recursive_search(numbers: List[int], target: int, start: int = 0) -> int:
    """Question 7: Recursive searching algorithm"""
    if start >= len(numbers):
        return -1
    if numbers[start] == target:
        return start
    return recursive_search(numbers, target, start + 1)

def generate_binary_number() -> tuple:
    """Question 8: Generate 4 digits number of 0s and 1s and convert to base 10"""
    binary = ''.join(str(random.randint(0, 1)) for _ in range(4))
    decimal = int(binary, 2)
    return binary, decimal

def fibonacci_sum(n: int = 50) -> int:
    """Question 9: Sum the first 50 fibonacci sequence"""
    def fibonacci():
        a, b = 0, 1
        while True:
            yield a
            a, b = b, a + b
    
    fib = fibonacci()
    return sum(next(fib) for _ in range(n))

def main():
    colors = [
        # Monday
        'GREEN', 'YELLOW', 'GREEN', 'BROWN', 'BLUE', 'PINK', 'BLUE', 'YELLOW', 
        'ORANGE', 'CREAM', 'ORANGE', 'RED', 'WHITE', 'BLUE', 'WHITE', 'BLUE', 
        'BLUE', 'BLUE', 'GREEN',
        # Tuesday
        'BROWN', 'GREEN', 'BROWN', 'BLUE', 'BLUE', 'BLUE', 'PINK', 'PINK',
        'ORANGE', 'ORANGE', 'RED', 'WHITE', 'BLUE', 'WHITE', 'WHITE', 'BLUE', 
        'BLUE', 'BLUE',
        # Wednesday
        'GREEN', 'YELLOW', 'GREEN', 'BROWN', 'BLUE', 'PINK', 'RED', 'YELLOW',
        'ORANGE', 'RED', 'ORANGE', 'RED', 'BLUE', 'BLUE', 'WHITE', 'BLUE',
        'BLUE', 'WHITE', 'WHITE',
        # Thursday
        'BLUE', 'BLUE', 'GREEN', 'WHITE', 'BLUE', 'BROWN', 'PINK', 'YELLOW',
        'ORANGE', 'CREAM', 'ORANGE', 'RED', 'WHITE', 'BLUE', 'WHITE', 'BLUE',
        'BLUE', 'BLUE', 'GREEN',
        # Friday
        'GREEN', 'WHITE', 'GREEN', 'BROWN', 'BLUE', 'BLUE', 'BLACK', 'WHITE',
        'ORANGE', 'RED', 'RED', 'RED', 'WHITE', 'BLUE', 'WHITE', 'BLUE',
        'BLUE', 'BLUE', 'WHITE'
    ]
    
    analyzer = ColorAnalyzer(colors)
    
    print("\nColor Analysis Results:")
    print(f"1. Mean color: {analyzer.get_mean_color()}")
    print(f"2. Most worn color: {analyzer.get_most_worn_color()}")
    print(f"3. Median color: {analyzer.get_median_color()}")
    print(f"4. Color variance: {analyzer.get_color_variance():.2f}")
    print(f"5. Probability of red: {analyzer.get_red_probability():.2%}")
    
    db_params = {
        'dbname': 'your_db_name',
        'user': 'your_username',
        'password': 'your_password',
        'host': 'localhost'
    }
    
   
    analyzer.save_to_postgresql(db_params)
    
    
    numbers = [1, 3, 5, 7, 9, 11, 13, 15]
    target = 7
    search_result = recursive_search(numbers, target)
    print(f"\nRecursive Search Result:")
    print(f"Found {target} at index: {search_result}")
    
   
    binary, decimal = generate_binary_number()
    print(f"\nBinary Number Generation:")
    print(f"Generated binary: {binary}")
    print(f"Decimal equivalent: {decimal}")
    
    
    fib_sum = fibonacci_sum()
    print(f"\nFibonacci Sum:")
    print(f"Sum of first 50 Fibonacci numbers: {fib_sum}")

if __name__ == "__main__":
    main()
