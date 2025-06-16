import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [transactions, setTransactions] = useState([]);
  const [rules, setRules] = useState([]);
  const [newRule, setNewRule] = useState({ name: '', condition: '', action: '' });
  const conditions = [
  "transaction.amount > 1000",
  "transaction.merchant == 'Unknown'",
  "transaction.credit_card_number.startswith('1234')"
  ];

  const actions = [
    "transaction.is_fraudulent = True",
    "print('Suspicious transaction detected')"
  ];
  useEffect(() => {
    fetchTransactions();
    fetchRules();
  }, []);

  const fetchTransactions = async () => {
    const response = await axios.get('http://localhost:8000/transactions/');
    setTransactions(response.data);
  };

  const fetchRules = async () => {
    const response = await axios.get('http://localhost:8000/rules/');
    setRules(response.data);
  };

  const handleRuleChange = (e) => {
    setNewRule({ ...newRule, [e.target.name]: e.target.value });
  };

  const handleRuleSubmit = async (e) => {
    e.preventDefault();
    await axios.post('http://localhost:8000/rules/', newRule);
    setNewRule({ name: '', condition: '', action: '' });
    fetchRules();
  };

  const applyRules = async () => {
    await axios.post('http://localhost:8000/apply-rules/');
    fetchTransactions();
  };
  const generateSampleData = async () => {
  await axios.post('http://localhost:8000/generate-sample-data/');
  fetchTransactions();
  };

  const deleteRule = async (ruleId) => {
  try {
    await axios.delete(`http://localhost:8000/rules/${ruleId}`);
    fetchRules(); // Refresh the rules list after deletion
  } catch (error) {
    console.error("Error deleting rule:", error);
  }
};

  return (
    <div className="App">
      <h1>Fraud Detection Rules Engine</h1>
      <button onClick={generateSampleData}>Generate Sample Data</button>
      <h2>Transactions</h2>
      <ul>
        {transactions.map(transaction => (
          <li key={transaction.id}>
            Amount: ${transaction.amount}, Merchant: {transaction.merchant}, 
            Fraudulent: {transaction.is_fraudulent ? 'Yes' : 'No'}
          </li>
        ))}
      </ul>

      <h2>Rules</h2>
      <ul>
        {rules.map(rule => (
          <li key={rule.id}>
            {rule.name}: {rule.condition} => {rule.action}
            <button onClick={() => deleteRule(rule.id)}>Delete</button>
          </li>
        ))}
      </ul>

      <h2>Create New Rule</h2>

      <form onSubmit={handleRuleSubmit}>
        <input
          name="name"
          value={newRule.name}
          onChange={handleRuleChange}
          placeholder="Rule Name"
        />
        <select name="condition" value={newRule.condition} onChange={handleRuleChange}>
          <option value="">Select a condition</option>
          {conditions.map((condition, index) => (
            <option key={index} value={condition}>{condition}</option>
          ))}
        </select>
        <select name="action" value={newRule.action} onChange={handleRuleChange}>
          <option value="">Select an action</option>
          {actions.map((action, index) => (
            <option key={index} value={action}>{action}</option>
          ))}
        </select>
        <button type="submit">Create Rule</button>
      </form>

      <button onClick={applyRules}>Apply Rules</button>
    </div>
  );
}

export default App;