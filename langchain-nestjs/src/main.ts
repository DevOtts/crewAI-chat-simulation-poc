import { NestFactory } from '@nestjs/core';
import { SimulationModule } from './modules/simulation.module';
import { SimulationService } from './services/simulation.service';

async function bootstrap() {
  const app = await NestFactory.create(SimulationModule);
  const simulation = app.get(SimulationService);
  
  await simulation.setupParticipants();
  await simulation.runSimulation();
}

bootstrap(); 