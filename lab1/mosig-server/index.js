import express from 'express';
import fs from 'fs';
import path from 'path';
import Mustache from 'mustache';
import data from './data/data.js';

const app = express();
const port = 3000;

// Serve static assets (images, CSS, JS) from assets/
app.use(express.static(path.join(process.cwd(), 'assets')));

app.get('/', (req, res) => {
  const filePath = path.join(process.cwd(), 'views', 'main.html');
  fs.readFile(filePath, 'utf8', (err, template) => {
    if (err) {
      if (err.code === 'ENOENT') {
        res.status(404).send('main.html not found');
      } else {
        res.status(500).send('Server error');
      }
    } else {
      const output = Mustache.render(template, data);
      res.send(output);
    }
  });
});

app.get('/categories', (req, res) => {
  const filePath = path.join(process.cwd(), 'views', 'categories.html');
  fs.readFile(filePath, 'utf8', (err, template) => {
    if (err) {
      if (err.code === 'ENOENT') {
        res.status(404).send('categories.html not found');
      } else {
        res.status(500).send('Server error');
      }
    } else {
      const output = Mustache.render(template, data);
      res.send(output);
    }
  });
});

// Dynamic route for categories - handles all category pages with one route
app.get('/categories/:categoryName', (req, res) => {
  const categoryName = req.params.categoryName;
  
  // Valid categories
  const validCategories = ['fruits', 'vegetables', 'virus', 'junk_food'];
  
  // Check if the requested category exists
  if (!validCategories.includes(categoryName)) {
    return res.status(404).send('Category not found');
  }
  
  const filePath = path.join(process.cwd(), 'views', 'category.html');
  fs.readFile(filePath, 'utf8', (err, template) => {
    if (err) {
      if (err.code === 'ENOENT') {
        res.status(404).send('category.html not found');
      } else {
        res.status(500).send('Server error');
      }
    } else {
      // Prepare data for the specific category
      const categoryData = {
        ...data,
        currentCategory: categoryName,
        // If your data.js has category-specific data, you can filter it here
        // For example: items: data.items.filter(item => item.category === categoryName)
      };
      
      const output = Mustache.render(template, categoryData);
      res.send(output);
    }
  });
});

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`);
});