import React, { useEffect, useState } from 'react';
import axios from 'axios';
import AddPipelineForm from './AddPipelineForm';

const BASE_URL = 'http://localhost:8000';

function App() {
  const [pipelines, setPipelines] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get(`${BASE_URL}/pipelines`)
      .then(response => {
        setPipelines(response.data);
        setLoading(false);
      })
      .catch(error => {
        alert("Ошибка при загрузке пайплайнов");
        setLoading(false);
      });
  }, []);

  const handleAddPipeline = (newPipeline) => {
    setPipelines([...pipelines, newPipeline]);
  };

  const handleRunPipeline = (pipelineId) => {
    axios.post(`${BASE_URL}/run/${pipelineId}`)
      .then(response => {
        alert(`Результаты запуска: ${response.data.stdout}`);
      })
      .catch(error => {
        alert("Ошибка при запуске пайплайна");
      });
  };

  const handleDeletePipeline = (pipelineId) => {
    axios.delete(`${BASE_URL}/pipelines/${pipelineId}`)
      .then(response => {
        setPipelines(pipelines.filter(p => p.id !== pipelineId));  // Обновляем список
      })
      .catch(error => {
        alert("Ошибка при удалении пайплайна");
      });
  };

  return (
    <div>
      <h1>Pipelines</h1>
      <AddPipelineForm onAdd={handleAddPipeline} />
      {loading ? <div>Загрузка...</div> : (
        <ul>
          {pipelines.map(pipeline => (
            <li key={pipeline.id}>
              {pipeline.name} — {pipeline.repo_url}
              <button onClick={() => handleRunPipeline(pipeline.id)}>Запустить</button>
              <button onClick={() => handleDeletePipeline(pipeline.id)}>Удалить</button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default App;
