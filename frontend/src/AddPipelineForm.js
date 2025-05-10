import React, { useState } from 'react';
import { TextField, Button, Box, Typography, Paper } from '@mui/material';
import axios from 'axios';

const AddPipelineForm = ({ onPipelineAdded }) => {
  const [name, setName] = useState('');
  const [repoUrl, setRepoUrl] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:8000/pipelines/', {
        name,
        repo_url: repoUrl,
      });
      onPipelineAdded(response.data);
      setName('');
      setRepoUrl('');
    } catch (error) {
      console.error('Ошибка при добавлении пайплайна:', error);
    }
  };

  return (
    <Paper elevation={3} sx={{ p: 3, mb: 4 }}>
      <Typography variant="h6" gutterBottom>Добавить пайплайн</Typography>
      <Box component="form" onSubmit={handleSubmit}>
        <TextField
          label="Название пайплайна"
          value={name}
          onChange={(e) => setName(e.target.value)}
          fullWidth
          margin="normal"
        />
        <TextField
          label="URL репозитория"
          value={repoUrl}
          onChange={(e) => setRepoUrl(e.target.value)}
          fullWidth
          margin="normal"
        />
        <Button type="submit" variant="contained" color="primary">
          Добавить
        </Button>
      </Box>
    </Paper>
  );
};

export default AddPipelineForm;
