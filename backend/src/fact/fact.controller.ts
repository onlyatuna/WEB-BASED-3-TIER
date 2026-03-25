import { Controller, Get, Post, Put, Delete, Body, Param } from '@nestjs/common';
import { FactService } from './fact.service';

@Controller('fact')
export class FactController {
  constructor(private readonly svc: FactService) {}

  @Get()
  findAll() { return this.svc.findAll(); }

  @Post()
  create(@Body() b: { fact_code: string; fact_name: string; remark: string }) {
    return this.svc.create(b.fact_code, b.fact_name, b.remark);
  }

  @Put(':id')
  update(@Param('id') id: string, @Body() b: { fact_name: string; remark: string }) {
    return this.svc.update(id, b.fact_name, b.remark);
  }

  @Delete(':id')
  remove(@Param('id') id: string) { return this.svc.remove(id); }
}
