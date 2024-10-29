import { Module } from '@nestjs/common';
import { SimulationService } from '../services/simulation.service';
import { AgentFactory } from '../agents/agent.factory';

@Module({
  providers: [SimulationService, AgentFactory],
  exports: [SimulationService],
})
export class SimulationModule {} 