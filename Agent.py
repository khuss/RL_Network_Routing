import numpy as np
import pandas as pd
import os
import random
import tensorflow as tf
from tensorflow.keras.optimizers.legacy import Adam
import tensorflow_probability as tfp
from networks import ActorCriticNetwork
from NetworkEnv import NetworkEnv as Ne
import matplotlib.pyplot as plt



class Agent:
    def __init__(self, env_name, alpha=0.00025, gamma=0.99, n_actions=[4,4,4,4,4]):
        self.gamma = gamma
        self.action_space = n_actions
        self.action = None
        self.actor_critic = ActorCriticNetwork(action_space=n_actions)
        self.env = Ne(env_name)



        self.actor_critic.compile(optimizer=Adam(learning_rate=alpha))

    def choose_action(self, observation):
        state = tf.convert_to_tensor([observation])
        _, probs = self.actor_critic(state)
        action_probabilities = tfp.distributions.Categorical(probs=probs)
        action = action_probabilities.sample()
        log_prob = action_probabilities.log_prob(action)
        self.action = action
        print(action)

        return action.numpy()


    def save_models(self):
        print('... saving models ...')
        self.actor_critic.save_weights(self.actor_critic.checkpoint_file)

    def load_models(self):
        print('... loading models ...')
        self.actor_critic.load_weights(self.actor_critic.checkpoint_file)

    def reset(self,df):
        self.env.reset(df)
        state = self.env.state_observation
        done = self.env.done
        reward = self.env.reward
        return state, done,reward





    def learn(self, state, reward, state_, done):
        state = tf.convert_to_tensor([state], dtype=tf.float32)
        state_ = tf.convert_to_tensor([state_], dtype=tf.float32)
        reward = tf.convert_to_tensor(reward, dtype=tf.float32)  # not fed to NN
        with tf.GradientTape(persistent=True) as tape:
            state_value, probs = self.actor_critic(state)
            state_value_, _ = self.actor_critic(state_)
            state_value = tf.squeeze(state_value)
            state_value_ = tf.squeeze(state_value_)

            action_probs = tfp.distributions.Categorical(probs=probs)
            log_prob = action_probs.log_prob(self.action)

            delta = reward + self.gamma * state_value_ * (1 - int(done)) - state_value
            actor_loss = -log_prob * delta
            critic_loss = delta ** 2
            total_loss = actor_loss + critic_loss

        gradient = tape.gradient(total_loss, self.actor_critic.trainable_variables)
        self.actor_critic.optimizer.apply_gradients(zip(
            gradient, self.actor_critic.trainable_variables))
        

    def run(self, df):
        # uncomment this line and do a mkdir tmp && mkdir video if you want to
        # record video of the agent playing the game.
        # env = wrappers.Monitor(env, 'tmp/video', video_callable=lambda episode_id: True, force=True)
        filename = 'results.png'

        figure_file = 'plots/' + filename

        best_score = -1000
        score_history = []
        load_checkpoint = False

        if load_checkpoint:
            self.load_models()

        for i in df:
            observation,done, score = self.reset(i)
            count = 0

            while not done:
                ohtob = preprocess(observation)
                action = self.choose_action(ohtob)
                observation_, reward, done, info = self.env.step(action, observation)
                score += reward
                ohtob_ = preprocess(observation_)
                print(score)
                print(action)
                print(observation)
                if not load_checkpoint:
                    self.learn(ohtob, reward, ohtob_, done)
                observation = observation_
                score_history.append(score)
                avg_score = np.mean(score_history[-100:])
                print(done)
                count +=1
                if count >200:
                  done = True
                  score -= 500
                
            

            
            if avg_score > best_score:
                best_score = avg_score
                if not load_checkpoint:
                    self.save_models()

            #print('episode ', i, 'score %.1f' % score, 'avg_score %.1f' % avg_score)

        if not load_checkpoint:
          N = len(score_history)
          running_avg = np.empty(N)
          for t in range(N):
            running_avg[t] = np.mean(scores[max(0, t - window):(t + 1)])
            if x is None:
              x = [i for i in range(N)]
            plt.ylabel('Score')
            plt.xlabel('Game')
            plt.plot(x, running_avg)
            plt.savefig(filename)

    def test(self, Model_name,df):
        self.load(Model_name)
        for e in range(100):
          state = self.reset(df)
          done = False
          score = 0
          while not done:
            print(done)
            one_hot_state = preprocess(state)
            one_hot_state = tf.convert_to_tensor([one_hot_state]) 
            prediction = self.Actor.predict(one_hot_state)
            action = np.zeros(5)
            count = 0
            for i in prediction:
              for j in i:
                action[count] = np.argmax(j)
                count +=1
            state, reward, done, _ = self.step(action)
            score += reward
            print(score)
 
          if done:
            print("episode: {}/{}, score: {}".format(e, self.EPISODES, score))
            print(average)
            break
        
      # close environemnt when finish training