import { Module } from '@nestjs/common';
import { FactController } from './fact.controller';
import { FactService } from './fact.service';

@Module({ controllers: [FactController], providers: [FactService] })
export class FactModule {}
