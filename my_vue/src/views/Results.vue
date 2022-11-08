<template>
    <v-content>
        <v-simple-table class="table">
            <template v-slot:default>
                <thead>
                <tr>
                    <th>Flights</th>
                    <th>Time</th>
                    <th>Price</th>
                </tr>
                </thead>
                <tbody>
                <tr
                    v-for="item in desserts"
                    :key="item.name"
                >
                    <td>{{ item.name }}</td>
                    <td>{{ item.calories }}</td>
                </tr>
                </tbody>
            </template>
        </v-simple-table>
    </v-content>
</template>
<script>
export default{
    name: 'Results',
    components:{

    },
    data () {
      return {
        desserts: [
          {
            name: 'Frozen Yogurt',
            calories: 159,
          },
          {
            name: 'Ice cream sandwich',
            calories: 237,
          },
          {
            name: 'Eclair',
            calories: 262,
          },
          {
            name: 'Cupcake',
            calories: 305,
          },
          {
            name: 'Gingerbread',
            calories: 356,
          },
          {
            name: 'Jelly bean',
            calories: 375,
          },
          {
            name: 'Lollipop',
            calories: 392,
          },
          {
            name: 'Honeycomb',
            calories: 408,
          },
          {
            name: 'Donut',
            calories: 452,
          },
          {
            name: 'KitKat',
            calories: 518,
          },
        ],
      }
    },
}
</script>

<style>

.table{
    padding-left: 20%;
    padding-right: 20%;

}

</style>
