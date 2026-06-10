import java.util.ArrayList;
import java.util.List;

class Account {
    private String accountNumber;
    private String ownerName;
    private double balance;

    public Account(String accountNumber, String ownerName) {
        this(accountNumber, ownerName, 0.0);
    }

    public Account(String accountNumber, String ownerName, double balance) {
        if (balance < 0) {
            throw new IllegalArgumentException("Initial balance cannot be negative.");
        }
        this.accountNumber = accountNumber;
        this.ownerName = ownerName;
        this.balance = balance;
    }

    public String getAccountNumber() { return accountNumber; }
    public void setAccountNumber(String accountNumber) { this.accountNumber = accountNumber; }
    
    public String getOwnerName() { return ownerName; }
    public void setOwnerName(String ownerName) { this.ownerName = ownerName; }
    
    public double getBalance() { return balance; }
    public void setBalance(double balance) { this.balance = balance; }

    public void deposit(double amount) {
        if (amount <= 0) {
            throw new IllegalArgumentException("Deposit amount must be positive.");
        }
        this.balance += amount;
    }

    public void withdraw(double amount) {
        if (amount <= 0) {
            throw new IllegalArgumentException("Withdrawal amount must be positive.");
        }
        if (amount > this.balance) {
            throw new IllegalStateException("Insufficient funds.");
        }
        this.balance -= amount;
    }

    public void display() {
        System.out.println("Account Number: " + accountNumber);
        System.out.println("Owner Name: " + ownerName);
        System.out.println("Balance: $" + balance);
    }
}

class SavingsAccount extends Account {
    private double interestRate;

    public SavingsAccount(String accountNumber, String ownerName, double balance, double interestRate) {
        super(accountNumber, ownerName, balance);
        this.interestRate = interestRate;
    }

    public double getInterestRate() { return interestRate; }
    public void setInterestRate(double interestRate) { this.interestRate = interestRate; }

    @Override
    public void display() {
        super.display(); 
        System.out.println("Interest Rate: " + interestRate + "%");
    }
}

class CurrentAccount extends Account {
    private double overdraftLimit;

    public CurrentAccount(String accountNumber, String ownerName, double balance, double overdraftLimit) {
        super(accountNumber, ownerName, balance);
        if (overdraftLimit < 0) {
            throw new IllegalArgumentException("Overdraft limit cannot be negative.");
        }
        this.overdraftLimit = overdraftLimit;
    }

    public double getOverdraftLimit() { return overdraftLimit; }
    public void setOverdraftLimit(double overdraftLimit) { this.overdraftLimit = overdraftLimit; }

    @Override
    public void withdraw(double amount) {
        if (amount <= 0) {
            throw new IllegalArgumentException("Withdrawal amount must be positive.");
        }
        if (getBalance() - amount < -overdraftLimit) {
            throw new IllegalStateException("Withdrawal exceeds overdraft limit.");
        }
        setBalance(getBalance() - amount); 
    }

    @Override
    public void display() {
        super.display();
        System.out.println("Overdraft Limit: $" + overdraftLimit);
    }
}

public class BankingSystem {
    public static void main(String[] args) {
        List<Account> accounts = new ArrayList<>();
        
        Account acc1 = new Account("A100", "Alice");
        SavingsAccount acc2 = new SavingsAccount("S200", "Bob", 1500.0, 4.5);
        CurrentAccount acc3 = new CurrentAccount("C300", "Charlie", 500.0, 1000.0);
        
        accounts.add(acc1);
        accounts.add(acc2);
        accounts.add(acc3);
        
        acc1.deposit(500.0);
        acc2.withdraw(200.0);
        acc3.withdraw(1200.0); 
        
        for (Account account : accounts) {
            account.display();
            System.out.println("---");
        }
    }
}