/**
 * Counter App - React Native
 * A digital counter with Theme Toggle functionality
 *
 * Features:
 * - Increment, Decrement, and Reset counter
 * - Light Mode / Dark Mode toggle
 * - Prevents negative counter values
 *
 * @format
 */

import React, {useState} from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  StatusBar,
} from 'react-native';

function App(): React.JSX.Element {
  // State for counter value (integer)
  const [count, setCount] = useState<number>(0);

  // State for active theme mode (boolean)
  const [isDarkMode, setIsDarkMode] = useState<boolean>(false);

  /**
   * Increment the counter by 1
   */
  const handleIncrement = (): void => {
    setCount(prevCount => prevCount + 1);
  };

  /**
   * Decrement the counter by 1
   * Constraint: Counter should never go below 0
   */
  const handleDecrement = (): void => {
    setCount(prevCount => {
      if (prevCount <= 0) {
        return 0; // Prevent negative numbers
      }
      return prevCount - 1;
    });
  };

  /**
   * Reset the counter back to 0
   */
  const handleReset = (): void => {
    setCount(0);
  };

  /**
   * Toggle between Light Mode and Dark Mode
   */
  const toggleTheme = (): void => {
    setIsDarkMode(prevMode => !prevMode);
  };

  // Dynamic styles based on current theme
  const dynamicContainerStyle = {
    backgroundColor: isDarkMode ? '#1a1a2e' : '#ffffff',
  };

  const dynamicTextStyle = {
    color: isDarkMode ? '#e0e0e0' : '#1a1a2e',
  };

  const dynamicCounterStyle = {
    color: isDarkMode ? '#ffffff' : '#000000',
  };

  const dynamicSubTextStyle = {
    color: isDarkMode ? '#8a8a9a' : '#666666',
  };

  return (
    <View style={[styles.container, dynamicContainerStyle]}>
      <StatusBar
        barStyle={isDarkMode ? 'light-content' : 'dark-content'}
        backgroundColor={isDarkMode ? '#1a1a2e' : '#ffffff'}
      />

      {/* App Title */}
      <Text style={[styles.title, dynamicTextStyle]}>Counter App</Text>

      {/* Counter Display */}
      <View style={styles.counterContainer}>
        <Text style={[styles.counterValue, dynamicCounterStyle]}>{count}</Text>
        <Text style={[styles.counterLabel, dynamicSubTextStyle]}>
          Current Count
        </Text>
      </View>

      {/* Increment and Decrement Buttons - Side by Side */}
      <View style={styles.buttonRow}>
        <TouchableOpacity
          style={[styles.button, styles.decrementButton]}
          onPress={handleDecrement}
          activeOpacity={0.7}>
          <Text style={styles.buttonText}>− Decrement</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={[styles.button, styles.incrementButton]}
          onPress={handleIncrement}
          activeOpacity={0.7}>
          <Text style={styles.buttonText}>+ Increment</Text>
        </TouchableOpacity>
      </View>

      {/* Reset Button */}
      <TouchableOpacity
        style={[styles.button, styles.resetButton]}
        onPress={handleReset}
        activeOpacity={0.7}>
        <Text style={styles.buttonText}>↺ Reset</Text>
      </TouchableOpacity>

      {/* Theme Toggle Button */}
      <TouchableOpacity
        style={[styles.button, styles.themeButton]}
        onPress={toggleTheme}
        activeOpacity={0.7}>
        <Text style={styles.buttonText}>
          {isDarkMode ? '☀ Switch to Light Mode' : '🌙 Switch to Dark Mode'}
        </Text>
      </TouchableOpacity>

      {/* Current Theme Indicator */}
      <Text style={[styles.themeIndicator, dynamicSubTextStyle]}>
        Current Theme: {isDarkMode ? 'Dark Mode' : 'Light Mode'}
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    marginBottom: 40,
  },
  counterContainer: {
    alignItems: 'center',
    marginBottom: 50,
  },
  counterValue: {
    fontSize: 80,
    fontWeight: 'bold',
    lineHeight: 90,
  },
  counterLabel: {
    fontSize: 16,
    marginTop: 8,
    letterSpacing: 1,
    textTransform: 'uppercase',
  },
  buttonRow: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 15,
    gap: 12,
  },
  button: {
    paddingVertical: 14,
    paddingHorizontal: 24,
    borderRadius: 12,
    minWidth: 150,
    alignItems: 'center',
    elevation: 3,
    shadowColor: '#000',
    shadowOffset: {width: 0, height: 2},
    shadowOpacity: 0.2,
    shadowRadius: 4,
  },
  incrementButton: {
    backgroundColor: '#4CAF50',
  },
  decrementButton: {
    backgroundColor: '#F44336',
  },
  resetButton: {
    backgroundColor: '#FF9800',
    marginBottom: 15,
    minWidth: 312,
  },
  themeButton: {
    backgroundColor: '#6200EE',
    minWidth: 312,
  },
  buttonText: {
    color: '#ffffff',
    fontSize: 16,
    fontWeight: '600',
  },
  themeIndicator: {
    marginTop: 30,
    fontSize: 14,
    fontStyle: 'italic',
  },
});

export default App;
