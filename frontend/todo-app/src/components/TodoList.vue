<template>
  <div>
    <h1>Todos</h1>
    <ul>
      <li v-for="todo in todos" :key="todo.id">
        {{ todo.title }}
        <input type="checkbox" v-model="todo.completed" @change="updateTodo(todo)">
        <button @click="updateTodo(todo)">Update</button>
        <button @click="deleteTodo(todo)">Delete</button>
      </li>
    </ul>
    <form @submit.prevent="createTodo">
      <input type="text" v-model="newTodo.title" placeholder="Title">
      <input type="text" v-model="newTodo.description" placeholder="Description">
      <button type="submit">{{ isUpdate ? 'Update' : 'Create' }}</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      todos: [],
      newTodo: {
        title: '',
        description: '',
        completed: 0
      },
      isUpdate: false
    }
  },
  mounted() {
    this.getTodos();
  },
  methods: {
    async getTodos() {
      try {
        const response = await axios.get('http://localhost:8000/todos');
        this.todos = response.data.todos;
      } catch (error) {
        console.error(error);
      }
    },
    async createTodo() {
      if (this.isUpdate) {
        try {
          const response = await axios.put(`http://localhost:8000/todos/${this.newTodo.id}`, this.newTodo);
          this.todos = this.todos.map(t => t.id === this.newTodo.id ? response.data.todo : t);
          this.newTodo = {
            title: '',
            description: '',
            completed: 0
          };
          this.isUpdate = false;
        } catch (error) {
          console.error(error);
        }
      } else {
        try {
          const response = await axios.post('http://localhost:8000/todos', this.newTodo);
          this.todos.push(response.data.todo);
          this.newTodo = {
            title: '',
            description: '',
            completed: 0
          };
        } catch (error) {
          console.error(error);
        }
      }
    },
    async updateTodo(todo) {
      this.newTodo = { ...todo };
      this.isUpdate = true;
    },
    async deleteTodo(todo) {
      try {
        await axios.delete(`http://localhost:8000/todos/${todo.id}`);
        this.todos = this.todos.filter(t => t.id !== todo.id);
      } catch (error) {
        console.error(error);
      }
    }
  }
}
</script>
