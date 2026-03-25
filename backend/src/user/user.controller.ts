import { Controller, Get, Post, Put, Delete, Body, Param } from '@nestjs/common';
import { UserService } from './user.service';

@Controller('user')
export class UserController {
  constructor(private readonly svc: UserService) {}

  @Get()
  findAll() { return this.svc.findAll(); }

  @Post()
  create(@Body() b: { userid: string; username: string; pwd: string }) {
    return this.svc.create(b.userid, b.username, b.pwd);
  }

  @Put(':id')
  update(@Param('id') id: string, @Body() b: { username: string; pwd: string }) {
    return this.svc.update(id, b.username, b.pwd);
  }

  @Delete(':id')
  remove(@Param('id') id: string) { return this.svc.remove(id); }
}
